const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}
const dropdownMenu1 = document.querySelectorAll(".dropdown-menu1");
const dropdownButton1 = document.querySelectorAll(".dropdown-button1");

function handleClick(event) {
  const main = event.target; // Use the event.target, the clicked element
  let myContent = null; // The drop down contents of the clicked item, if found
  dropdownMenu1.forEach( elem => {
    // Kludge: using parentNode since the clicked element is in it's own div.
    // It would probably be better if the querySelector above selected
    // the li-element, and then remove paretNode from the next statement.
    if ( main.parentNode.parentNode.contains(elem)) {
      myContent = elem;
    } else {
      // Remove the class from every content except the clicked one.
      elem.classList.remove('show');
    }
  });
  // If the clicked have content, troggle if it is shown or not.
  if (myContent) myContent.classList.toggle('show');
}

dropdownButton1.forEach( elem => elem.addEventListener("click",  handleClick));


// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;

function showAlert() {
  var myText = "You can't bid on your own offer";
  alert (myText);
}




function setHeight(){
    var offsetHeight = document.getElementById('topics').parentElement.offsetHeight;
    document.getElementById('topics').style.height = offsetHeight+'px';
    document.getElementById('wrapper').style.height = offsetHeight+'px';
  }
setHeight()
