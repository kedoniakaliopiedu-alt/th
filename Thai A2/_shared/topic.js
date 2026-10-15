(() => {
  const fitExample = (example) => {
    const units = [...example.querySelectorAll(
      ':scope > .example-unit, :scope > .example-item'
    )];
    if (!units.length) return;

    example.style.fontSize = '';
    const maximum = parseFloat(getComputedStyle(example).fontSize);
    const minimum = 10;
    const available = example.clientWidth;
    const fits = (size) => {
      example.style.fontSize = `${size}px`;
      return units.every((unit) => unit.scrollWidth <= available + 1);
    };

    if (fits(maximum)) return;
    let low = minimum;
    let high = maximum;
    for (let step = 0; step < 12; step += 1) {
      const middle = (low + high) / 2;
      if (fits(middle)) low = middle;
      else high = middle;
    }
    example.style.fontSize = `${low}px`;
  };

  const fitAllExamples = () => {
    document.querySelectorAll('.example-list, .example-lines, .fit-lines').forEach(fitExample);
  };

  let resizeFrame = 0;
  window.addEventListener('resize', () => {
    cancelAnimationFrame(resizeFrame);
    resizeFrame = requestAnimationFrame(fitAllExamples);
  });
  document.addEventListener('toggle', (event) => {
    if (event.target instanceof HTMLDetailsElement && event.target.open) {
      requestAnimationFrame(fitAllExamples);
    }
  }, true);
  window.addEventListener('beforeprint', fitAllExamples);
  fitAllExamples();
  document.fonts?.ready.then(fitAllExamples);
})();
