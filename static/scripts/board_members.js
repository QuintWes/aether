document.addEventListener("DOMContentLoaded", function() {
    const loadMoreBtn = document.getElementById("loadMoreBtn");
    let visibleProjects = 6; // Tracks the number of visible projects initially
    let previouslyVisible = 6; // Tracks the previously visible projects
    const allProjects = document.querySelectorAll(".project-card-parent");

    loadMoreBtn.addEventListener("click", function() {
        for (let i = visibleProjects; i < visibleProjects + 6; i++) {
            if (allProjects[i]) {
                allProjects[i].classList.remove("d-none");
            }
        }
        previouslyVisible = visibleProjects; // Update the previously visible count
        visibleProjects += 6;

        if (visibleProjects >= allProjects.length) {
            loadMoreBtn.style.display = "none";
        }

        console.log(previouslyVisible);
        // Apply GSAP animation to newly revealed projects only
        gsap.from(".project-card-parent:not(.d-none):nth-child(n + " + (previouslyVisible + 1) + "):nth-child(-n + " + visibleProjects + ")", {
            opacity: 0,
            y: 100,
            duration: 1,
            stagger: 0.2, // Adjust the stagger value for timing between animations
            ease: "power4.out" // Easing function
        });
    });
});



gsap.from(".project-card-parent", {
            opacity: 0,
            y: 100,
            duration: 1,
            stagger: 0.2, // Adjust the stagger value for timing between animations
            ease: "power4.out" // Easing function
        });
