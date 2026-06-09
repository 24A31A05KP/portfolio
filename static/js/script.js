// ================= SCROLL REVEAL =================
const reveals =
document.querySelectorAll(".reveal");

window.addEventListener(
    "scroll",
    revealSections
);

function revealSections(){

    const triggerBottom =
        window.innerHeight * 0.85;

    reveals.forEach(section => {

        const sectionTop =
            section.getBoundingClientRect().top;

        if(sectionTop < triggerBottom){
            section.classList.add("active");
        }
    });
}

revealSections();
// ================= ACTIVE NAVBAR =================
const sections =
document.querySelectorAll("section");

const navLinks =
document.querySelectorAll(
    ".nav-links a"
);

window.addEventListener(
    "scroll",
    () => {

    let current = "";

    sections.forEach(section => {

        const sectionTop =
            section.offsetTop;

        const sectionHeight =
            section.clientHeight;

        if(
            pageYOffset >=
            sectionTop - 200
        ){
            current =
            section.getAttribute("id");
        }
    });

    navLinks.forEach(link => {

        link.classList.remove(
            "active"
        );

        if(
            link.getAttribute("href")
            === `#${current}`
        ){
            link.classList.add(
                "active"
            );
        }
    });
});
// ================= TYPING EFFECT =================
const typingText =
document.getElementById(
    "typing-text"
);

const roles = [

    "Aspiring Software Developer",

    "Python Developer",

    "Frontend Learner",

    "DSA Enthusiast"

];

let roleIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeEffect(){

    const currentRole =
        roles[roleIndex];

    if(!isDeleting){

        typingText.textContent =
        currentRole.substring(
            0,
            charIndex++
        );

    }else{

        typingText.textContent =
        currentRole.substring(
            0,
            charIndex--
        );
    }

    let speed =
        isDeleting ? 50 : 100;

    if(
        !isDeleting &&
        charIndex ===
        currentRole.length + 1
    ){

        speed = 1500;
        isDeleting = true;
    }

    else if(
        isDeleting &&
        charIndex === 0
    ){

        isDeleting = false;

        roleIndex =
        (roleIndex + 1)
        % roles.length;
    }

    setTimeout(
        typeEffect,
        speed
    );
}

typeEffect();
// MOBILE MENU TEST
document.addEventListener(
    "DOMContentLoaded",
    function(){

        const menu =
        document.getElementById(
            "menu-toggle"
        );

        const nav =
        document.querySelector(
            ".nav-links"
        );

        console.log("JS WORKING");

        menu.addEventListener(
            "click",
            function(){

                nav.classList.toggle(
                    "active"
                );

                console.log("CLICKED");
            }
        );
    }
);