// Use case scoring exercise: the learner computes the weighted score and picks the decision.
//
// Markup:
//   <div class="scorer" data-name="Bag tracking" data-scores="4,1,2,3,3,5" data-confidence="High"
//        data-weights="25,25,15,10,15,10"></div>      (data-weights optional; defaults below)
//
// Rules, from skills/discovery-use-case-scoring/SKILL.md:
//   weighted = sum(score × weight) / 100
//   >= 3.5 and High -> Build first; >= 3.5 otherwise -> Prototype to learn
//   2.5 to 3.4 -> Defer; below 2.5 -> Drop

const DIMENSIONS = ["Pain", "Outcome", "Reach", "Fit", "Feasibility", "Adoption"];
const DEFAULT_WEIGHTS = [25, 25, 15, 10, 15, 10];
const DECISIONS = ["Build first", "Prototype to learn", "Defer", "Drop"];

function decide(weighted, confidence) {
  if (weighted >= 3.5) return confidence === "High" ? "Build first" : "Prototype to learn";
  if (weighted >= 2.5) return "Defer";
  return "Drop";
}

// Small element builder: el("td", {className: "x"}, "text", childNode, ...)
function el(tag, props = {}, ...children) {
  const node = Object.assign(document.createElement(tag), props);
  children.forEach((c) => node.append(c));
  return node;
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".scorer").forEach((box) => {
    const scores = box.dataset.scores.split(",").map(Number);
    const weights = box.dataset.weights ? box.dataset.weights.split(",").map(Number) : DEFAULT_WEIGHTS;
    const confidence = box.dataset.confidence;
    const weighted = scores.reduce((sum, s, i) => sum + s * weights[i], 0) / 100;
    const decision = decide(weighted, confidence);
    const working = `(${scores.map((s, i) => `${s}×${weights[i]}`).join(" + ")}) ÷ 100`;

    const headRow = el("tr", {}, ...DIMENSIONS.map((d, i) => el("th", {}, d, el("br"), el("small", {}, String(weights[i])))), el("th", {}, "Confidence"));
    const bodyRow = el("tr", {}, ...scores.map((s) => el("td", {}, String(s))), el("td", {}, confidence));
    const input = el("input", { type: "number", step: "0.05", min: "1", max: "5", inputMode: "decimal" });
    const select = el("select", {}, el("option", { value: "" }, "choose"), ...DECISIONS.map((d) => el("option", {}, d)));
    const check = el("button", { type: "button", className: "check" }, "Check");
    const feedback = el("div", { className: "feedback" });
    feedback.setAttribute("aria-live", "polite");

    box.replaceChildren(
      el("div", { className: "stem" }, box.dataset.name),
      el("table", {}, el("thead", {}, headRow), el("tbody", {}, bodyRow)),
      el("label", {}, "Weighted score ", input),
      el("label", {}, "Decision ", select),
      check,
      feedback,
    );

    check.addEventListener("click", () => {
      const scoreOk = Math.abs(Number(input.value) - weighted) < 0.001;
      const decisionOk = select.value === decision;
      feedback.className = "feedback " + (scoreOk && decisionOk ? "right" : "wrong");
      feedback.textContent = scoreOk && decisionOk
        ? `Right: ${weighted.toFixed(2)}, ${decision}.`
        : `${scoreOk ? "Score right." : `Score: ${working} = ${weighted.toFixed(2)}.`} ` +
          `${decisionOk ? "Decision right." : `Decision: ${decision} (${weighted.toFixed(2)} with ${confidence} confidence).`}`;
    });
  });
});
