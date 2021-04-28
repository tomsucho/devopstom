const backdrop = document.getElementById("backdrop");
const loginBtn = document.getElementById('nav-login-btn');
const modalLoginCard = document.getElementById("modal-login-card");
const cancelLoginBtn = document.getElementById("cancel-login-btn");

const toggleBackdrop = () => {
  backdrop.classList.toggle("visible");
};

const loginHandler = () => {
  toggleBackdrop();
  modalLoginCard.classList.add("visible");
};

const closeLoginHandler = () => {
  toggleBackdrop();
  modalLoginCard.classList.remove("visible");
};

loginBtn.addEventListener("click", loginHandler);
cancelLoginBtn.addEventListener("click", closeLoginHandler);
