document.addEventListener("DOMContentLoaded", function () {
  const papers = document.querySelectorAll(".paper");
  papers.forEach((paper, index) => {
    paper.style.animationDelay = `${index * 0.5}s`;
  });
});
