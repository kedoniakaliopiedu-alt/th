// thaiocr — локальный инструмент распознавания тайского письма.
// Работает офлайн на встроенных macOS-фреймворках: Vision (OCR, th-TH) + CoreImage (предобработка).
// Ничего не устанавливает и никуда не ходит по сети.
//
// Сборка и запуск — через обёртку ./thaiocr (компилирует при первом вызове).

import Foundation
import CoreImage
import CoreGraphics
import ImageIO
import Vision

// MARK: - Утилиты

func fail(_ msg: String) -> Never {
    FileHandle.standardError.write(("thaiocr: " + msg + "\n").data(using: .utf8)!)
    exit(1)
}

func makeContext() -> CIContext {
    CIContext(options: [.workingColorSpace: CGColorSpaceCreateDeviceRGB()])
}

/// Загружает изображение с учётом EXIF-ориентации (фото с телефона часто лежат «боком»).
func loadImage(_ path: String) -> CIImage {
    let url = URL(fileURLWithPath: (path as NSString).expandingTildeInPath)
    guard FileManager.default.fileExists(atPath: url.path) else { fail("файл не найден: \(path)") }
    guard let img = CIImage(contentsOf: url, options: [.applyOrientationProperty: true]) else {
        fail("не удалось прочитать изображение: \(path)")
    }
    return img.transformed(by: CGAffineTransform(translationX: -img.extent.origin.x,
                                                 y: -img.extent.origin.y))
}

func writePNG(_ image: CIImage, to path: String) {
    let img = image.transformed(by: CGAffineTransform(translationX: -image.extent.origin.x,
                                                      y: -image.extent.origin.y))
    let url = URL(fileURLWithPath: (path as NSString).expandingTildeInPath)
    try? FileManager.default.createDirectory(at: url.deletingLastPathComponent(),
                                             withIntermediateDirectories: true)
    guard let cs = CGColorSpace(name: CGColorSpace.sRGB) else { fail("нет sRGB") }
    do {
        try makeContext().writePNGRepresentation(of: img, to: url, format: .RGBA8, colorSpace: cs)
    } catch {
        fail("не удалось записать \(path): \(error)")
    }
}

func cgImage(_ image: CIImage) -> CGImage {
    guard let cg = makeContext().createCGImage(image, from: image.extent) else {
        fail("не удалось растеризовать изображение")
    }
    return cg
}

func jsonString(_ any: Any) -> String {
    guard let data = try? JSONSerialization.data(withJSONObject: any,
                                                 options: [.prettyPrinted, .sortedKeys,
                                                           .withoutEscapingSlashes]),
          let s = String(data: data, encoding: .utf8) else { return "{}" }
    return s
}

// MARK: - Предобработка

func scaled(_ image: CIImage, by factor: Double) -> CIImage {
    guard factor != 1.0, let f = CIFilter(name: "CILanczosScaleTransform") else { return image }
    f.setValue(image, forKey: kCIInputImageKey)
    f.setValue(factor, forKey: kCIInputScaleKey)
    f.setValue(1.0, forKey: kCIInputAspectRatioKey)
    return f.outputImage ?? image
}

/// CIDocumentEnhancer — «скан документа»: выравнивает фон, вытягивает штрих.
/// Лучший из доступных фильтров для тетрадного листа, снятого на телефон.
func enhanced(_ image: CIImage, amount: Double) -> CIImage {
    guard let f = CIFilter(name: "CIDocumentEnhancer") else { return image }
    f.setValue(image, forKey: kCIInputImageKey)
    f.setValue(amount, forKey: "inputAmount")
    return f.outputImage ?? image
}

func mono(_ image: CIImage, contrast: Double) -> CIImage {
    guard let f = CIFilter(name: "CIColorControls") else { return image }
    f.setValue(image, forKey: kCIInputImageKey)
    f.setValue(0.0, forKey: kCIInputSaturationKey)
    f.setValue(contrast, forKey: kCIInputContrastKey)
    return f.outputImage ?? image
}

func rotated(_ image: CIImage, radians: Double) -> CIImage {
    guard radians != 0 else { return image }
    let t = CGAffineTransform(translationX: image.extent.midX, y: image.extent.midY)
    let m = CGAffineTransform(translationX: -image.extent.midX, y: -image.extent.midY)
        .concatenating(CGAffineTransform(rotationAngle: radians))
        .concatenating(t)
    return image.transformed(by: m)
}

// MARK: - Vision

struct Line {
    let text: String
    let candidates: [String]
    let confidence: Float
    /// Нормализованный bbox Vision: origin — левый НИЖНИЙ угол.
    let box: CGRect
    let angle: Double
}

func recognize(_ image: CIImage,
               langs: [String],
               correction: Bool,
               customWords: [String],
               minHeight: Float) -> [Line] {
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = langs
    request.usesLanguageCorrection = correction
    request.minimumTextHeight = minHeight
    if !customWords.isEmpty { request.customWords = customWords }

    let handler = VNImageRequestHandler(cgImage: cgImage(image), options: [:])
    do { try handler.perform([request]) } catch { fail("Vision: \(error)") }

    let observations = request.results ?? []
    return observations.map { obs in
        let cands = obs.topCandidates(3)
        let angle: Double = {
            let dx = obs.topRight.x - obs.topLeft.x
            let dy = obs.topRight.y - obs.topLeft.y
            return atan2(Double(dy), Double(dx))
        }()
        return Line(text: cands.first?.string ?? "",
                    candidates: cands.map { $0.string },
                    confidence: cands.first?.confidence ?? 0,
                    box: obs.boundingBox,
                    angle: angle)
    }
    .sorted { $0.box.midY > $1.box.midY }   // сверху вниз
}

/// Нормализованный bbox Vision → пиксельный прямоугольник в системе CIImage (origin — левый нижний).
func pixelRect(_ box: CGRect, in extent: CGRect, padX: Double, padY: Double) -> CGRect {
    var r = VNImageRectForNormalizedRect(box, Int(extent.width), Int(extent.height))
    let dx = r.width * padX, dy = r.height * padY
    r = r.insetBy(dx: -dx, dy: -dy)
    return r.intersection(extent)
}

// MARK: - Разбор аргументов

struct Args {
    var positional: [String] = []
    var flags: [String: String] = [:]

    init(_ argv: [String]) {
        var i = 0
        while i < argv.count {
            let a = argv[i]
            if a.hasPrefix("--") {
                let key = String(a.dropFirst(2))
                if i + 1 < argv.count && !argv[i + 1].hasPrefix("--") {
                    flags[key] = argv[i + 1]; i += 2
                } else {
                    flags[key] = "true"; i += 1
                }
            } else {
                positional.append(a); i += 1
            }
        }
    }

    func str(_ k: String, _ d: String) -> String { flags[k] ?? d }
    func num(_ k: String, _ d: Double) -> Double { flags[k].flatMap(Double.init) ?? d }
    func bool(_ k: String) -> Bool { flags[k] == "true" }
    func at(_ i: Int, _ name: String) -> String {
        guard i < positional.count else { fail("не хватает аргумента: \(name)") }
        return positional[i]
    }
}

/// Словарь для подсказки Vision: либо .txt (по слову в строке), либо progress.json проекта.
func loadCustomWords(_ path: String) -> [String] {
    guard !path.isEmpty else { return [] }
    let url = URL(fileURLWithPath: (path as NSString).expandingTildeInPath)
    guard let data = try? Data(contentsOf: url) else { fail("не читается словарь: \(path)") }
    if path.hasSuffix(".json"),
       let root = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
       let items = root["items"] as? [String: Any] {
        return Array(items.keys)
    }
    let text = String(data: data, encoding: .utf8) ?? ""
    return text.split(whereSeparator: \.isNewline).map(String.init).filter { !$0.isEmpty }
}

// MARK: - Команды

func cmdOCR(_ args: Args) {
    let image = loadImage(args.at(1, "<image>"))
    let langs = args.str("langs", "th-TH").split(separator: ",").map(String.init)
    let lines = recognize(image,
                          langs: langs,
                          correction: !args.bool("no-correct"),
                          customWords: loadCustomWords(args.str("words-from", "")),
                          minHeight: Float(args.num("min-height", 0.0)))
    if args.bool("json") {
        let payload: [String: Any] = [
            "image": args.at(1, "<image>"),
            "width": Int(image.extent.width), "height": Int(image.extent.height),
            "lines": lines.enumerated().map { (i, l) -> [String: Any] in
                ["index": i + 1, "text": l.text, "confidence": Double(l.confidence),
                 "candidates": l.candidates,
                 "box": ["x": l.box.origin.x, "y": l.box.origin.y,
                         "w": l.box.width, "h": l.box.height]]
            }
        ]
        print(jsonString(payload))
    } else {
        if lines.isEmpty { print("(Vision не нашёл строк — рукопись слишком неконтрастная или мелкая)") }
        for (i, l) in lines.enumerated() {
            print(String(format: "%2d  [%.2f]  %@", i + 1, l.confidence, l.text))
            for alt in l.candidates.dropFirst() { print("             ~ \(alt)") }
        }
    }
}

func cmdPrep(_ args: Args) {
    var image = loadImage(args.at(1, "<in>"))
    let out = args.at(2, "<out.png>")

    if args.bool("deskew") {
        let lines = recognize(image, langs: ["th-TH"], correction: false, customWords: [], minHeight: 0)
        let angles = lines.map(\.angle).filter { abs($0) < 0.35 }.sorted()
        if !angles.isEmpty {
            let median = angles[angles.count / 2]
            image = rotated(image, radians: -median)
            FileHandle.standardError.write(
                String(format: "deskew: %.2f°\n", -median * 180 / .pi).data(using: .utf8)!)
        }
    }
    if !args.bool("no-enhance") { image = enhanced(image, amount: args.num("enhance", 1.0)) }
    if args.bool("mono") || args.flags["contrast"] != nil {
        image = mono(image, contrast: args.num("contrast", 1.4))
    }
    image = scaled(image, by: args.num("scale", 2.0))
    writePNG(image, to: out)
    print("\(out)  \(Int(image.extent.width))×\(Int(image.extent.height))")
}

func cmdLines(_ args: Args) {
    let source = args.at(1, "<in>")
    let outDir = args.at(2, "<outdir>")
    var image = loadImage(source)
    if !args.bool("no-enhance") { image = enhanced(image, amount: args.num("enhance", 1.0)) }
    let extent = image.extent

    let lines = recognize(image,
                          langs: args.str("langs", "th-TH").split(separator: ",").map(String.init),
                          correction: !args.bool("no-correct"),
                          customWords: loadCustomWords(args.str("words-from", "")),
                          minHeight: Float(args.num("min-height", 0.0)))

    let scale = args.num("scale", 4.0)
    let padX = args.num("pad-x", 0.02), padY = args.num("pad-y", 0.35)
    var manifest: [[String: Any]] = []

    var rects: [(CGRect, Line?)] = lines.map { (pixelRect($0.box, in: extent, padX: padX, padY: padY), $0) }

    // Запасной вариант: Vision не увидел строк (типично для «петельного» почерка) —
    // режем лист на горизонтальные полосы с перехлёстом, чтобы читать глазами.
    if rects.isEmpty {
        let bands = max(2, Int(args.num("bands", 10)))
        let h = extent.height / Double(bands)
        rects = (0..<bands).map { i in
            let y = extent.height - Double(i + 1) * h
            return (CGRect(x: 0, y: max(0, y - h * 0.15), width: extent.width, height: h * 1.3)
                        .intersection(extent), nil)
        }
    }

    for (i, pair) in rects.enumerated() {
        let (rect, line) = pair
        guard rect.width > 4, rect.height > 4 else { continue }
        let crop = image.cropped(to: rect)
        let out = "\(outDir)/line-\(String(format: "%02d", i + 1)).png"
        writePNG(scaled(crop, by: scale), to: out)
        var entry: [String: Any] = ["index": i + 1, "file": out]
        if let l = line {
            entry["vision_text"] = l.text
            entry["confidence"] = Double(l.confidence)
            entry["candidates"] = l.candidates
        } else {
            entry["vision_text"] = NSNull()
            entry["note"] = "полоса (Vision не распознал строки)"
        }
        manifest.append(entry)
        print(String(format: "%@  [%.2f]  %@", out,
                     Double(line?.confidence ?? 0), line?.text ?? "—"))
    }

    let manifestPath = "\(outDir)/lines.json"
    let payload: [String: Any] = ["source": source, "count": manifest.count, "lines": manifest]
    try? jsonString(payload).write(toFile: (manifestPath as NSString).expandingTildeInPath,
                                   atomically: true, encoding: .utf8)
    print("\n\(manifestPath)")
}

func cmdCrop(_ args: Args) {
    let image = loadImage(args.at(1, "<in>"))
    let out = args.at(2, "<out.png>")
    let parts = args.str("rect", "").split(separator: ",").compactMap { Double($0) }
    guard parts.count == 4 else { fail("нужен --rect x,y,w,h (пиксели, начало отсчёта — левый ВЕРХНИЙ угол)") }
    // из системы «сверху вниз» в систему CoreImage «снизу вверх»
    let rect = CGRect(x: parts[0], y: image.extent.height - parts[1] - parts[3],
                      width: parts[2], height: parts[3]).intersection(image.extent)
    guard !rect.isEmpty else { fail("--rect вне изображения") }
    var crop = image.cropped(to: rect)
    if !args.bool("no-enhance") { crop = enhanced(crop, amount: args.num("enhance", 1.0)) }
    writePNG(scaled(crop, by: args.num("scale", 4.0)), to: out)
    print("\(out)")
}

func cmdLangs() {
    let r = VNRecognizeTextRequest()
    r.recognitionLevel = .accurate
    let langs = (try? r.supportedRecognitionLanguages()) ?? []
    print(langs.joined(separator: " "))
    print(langs.contains("th-TH") ? "\nth-TH: поддерживается" : "\nth-TH: НЕ поддерживается на этой macOS")
}

let usage = """
thaiocr — распознавание тайского письма на встроенном Vision (офлайн)

  thaiocr ocr   <image> [--langs th-TH,en-US] [--no-correct] [--words-from progress.json]
                        [--min-height 0.0] [--json]
      OCR всей страницы. Печатает строки с уверенностью и альтернативами.

  thaiocr lines <image> <outdir> [--scale 4] [--pad-y 0.35] [--words-from progress.json]
                        [--bands 10] [--no-enhance]
      Режет страницу на строки и сохраняет каждую крупным PNG + lines.json.
      Главный режим для рукописи: строки читаются глазами по одной.

  thaiocr prep  <in> <out.png> [--scale 2] [--deskew] [--mono] [--contrast 1.4]
                        [--enhance 1.0] [--no-enhance]
      Предобработка: выравнивание наклона, «скан документа», ч/б, апскейл.

  thaiocr crop  <in> <out.png> --rect x,y,w,h [--scale 4]
      Вырезать и увеличить фрагмент (координаты от левого ВЕРХНЕГО угла).

  thaiocr langs
      Языки OCR, доступные в этой системе.
"""

@main
struct ThaiOCR {
    static func main() {
        let args = Args(Array(CommandLine.arguments.dropFirst()))
        switch args.positional.first {
        case "ocr":   cmdOCR(args)
        case "lines": cmdLines(args)
        case "prep":  cmdPrep(args)
        case "crop":  cmdCrop(args)
        case "langs": cmdLangs()
        default:      print(usage)
        }
    }
}
