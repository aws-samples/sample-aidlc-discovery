// Multiple-choice quiz with immediate feedback.
//
// Markup:
//   <div class="quiz" data-correct="2">        (0-based index of the right option)
//     <div class="stem">Question?</div>
//     <div class="opts"><button class="opt">A</button> ... </div>
//     <div class="why">Explanation, shown after the first answer.</div>
//   </div>
//   <p class="quiz-score"></p>                  (optional running score)

document.addEventListener("DOMContentLoaded", () => {
  const quizzes = [...document.querySelectorAll(".quiz")];
  const scoreEl = document.querySelector(".quiz-score");
  let answered = 0;
  let right = 0;

  const updateScore = () => {
    if (!scoreEl) return;
    scoreEl.textContent = answered === quizzes.length
      ? `${right} of ${quizzes.length} right on the first try. Come back in a few days and try again without reading the lesson.`
      : `${answered} of ${quizzes.length} answered.`;
  };

  quizzes.forEach((quiz) => {
    const correct = Number(quiz.dataset.correct);
    const opts = [...quiz.querySelectorAll("button.opt")];
    opts.forEach((btn, i) => {
      btn.type = "button";
      btn.addEventListener("click", () => {
        if (quiz.classList.contains("done")) return;
        quiz.classList.add("done");
        answered += 1;
        if (i === correct) right += 1;
        opts.forEach((b, j) => {
          b.disabled = true;
          if (j === correct) b.classList.add("right");
          else if (j === i) b.classList.add("wrong");
        });
        updateScore();
      });
    });
  });

  updateScore();
});
