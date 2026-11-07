// Renders every chart on the page from the JSON block written by src/build.py.
// Colours come from CSS custom properties, so charts follow light/dark mode.
(function () {
  var dataEl = document.getElementById("chart-data");
  if (!dataEl || typeof Plotly === "undefined") return;
  var specs = JSON.parse(dataEl.textContent);

  function cssVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function theme() {
    return {
      text: cssVar("--text"),
      text2: cssVar("--text-2"),
      muted: cssVar("--muted"),
      grid: cssVar("--grid"),
      surface: cssVar("--surface"),
      series: [cssVar("--series-1"), cssVar("--series-2"), cssVar("--series-3"), cssVar("--series-4")]
    };
  }

  function clone(o) { return JSON.parse(JSON.stringify(o)); }

  function build(spec, t) {
    var traces = spec.traces.map(function (tr) {
      var out = clone(tr);
      var c = tr.color === "muted" ? t.muted : t.series[(tr.color || 1) - 1];
      delete out.color;
      if (out.type === "bar") {
        out.marker = Object.assign({ color: c, line: { color: t.surface, width: 1 } }, out.marker || {});
      } else {
        out.line = Object.assign({ color: c, width: 2 }, out.line || {});
        out.marker = Object.assign({ color: c, size: 8, line: { color: t.surface, width: 2 } }, out.marker || {});
        if (out.marker.symbol && /open/.test(out.marker.symbol)) { out.marker.line = { color: c, width: 2 }; }
      }
      if (out.textfont === undefined) out.textfont = { color: t.text2, size: 11 };
      return out;
    });
    var axis = {
      gridcolor: t.grid, zerolinecolor: t.grid, linecolor: t.grid,
      tickfont: { color: t.text2, size: 12 }, title: { font: { color: t.text2, size: 12 } },
      automargin: true, fixedrange: true
    };
    var layout = {
      paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
      font: { family: getComputedStyle(document.body).fontFamily, color: t.text, size: 12 },
      margin: { l: 10, r: 14, t: traces.length > 1 ? 48 : 18, b: 10 },
      hovermode: "closest",
      hoverlabel: { bgcolor: t.surface, bordercolor: t.grid, font: { color: t.text } },
      showlegend: traces.length > 1,
      legend: { orientation: "h", x: 0, y: 1.02, yanchor: "bottom", font: { color: t.text2 } },
      xaxis: Object.assign({}, axis), yaxis: Object.assign({}, axis),
      bargap: 0.25
    };
    var L = clone(spec.layout || {});
    ["xaxis", "yaxis"].forEach(function (k) {
      if (L[k]) {
        if (L[k].title && typeof L[k].title === "string") L[k].title = { text: L[k].title, font: { color: t.text2, size: 12 } };
        layout[k] = Object.assign({}, layout[k], L[k]);
        delete L[k];
      }
    });
    if (L.annotations) {
      L.annotations.forEach(function (a) {
        a.font = Object.assign({ color: t.text2, size: 11 }, a.font || {});
        a.arrowcolor = t.muted;
      });
    }
    if (L.legend) { layout.legend = Object.assign({}, layout.legend, L.legend); delete L.legend; }
    Object.assign(layout, L);
    return { traces: traces, layout: layout };
  }

  function renderAll() {
    var t = theme();
    document.querySelectorAll(".plot[data-chart]").forEach(function (el) {
      var spec = specs[el.getAttribute("data-chart")];
      if (!spec) return;
      var b = build(spec, t);
      Plotly.react(el, b.traces, b.layout, { responsive: true, displayModeBar: false });
    });
  }

  renderAll();
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq.addEventListener) mq.addEventListener("change", renderAll);
    else if (mq.addListener) mq.addListener(renderAll);
  }
})();
