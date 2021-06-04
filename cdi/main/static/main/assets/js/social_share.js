/*
Social Share Links:
WhatsApp:
https://wa.me/?text=[post-title] [post-url]
Facebook:
https://www.facebook.com/sharer.php?u=[post-url]
Twitter:
https://twitter.com/share?url=[post-url]&text=[post-title]
Pinterest:
https://pinterest.com/pin/create/bookmarklet/?media=[post-img]&url=[post-url]&is_video=[is_video]&description=[post-title]
LinkedIn:
https://www.linkedin.com/shareArticle?url=[post-url]&title=[post-title]
*/

const facebookBtn = document.querySelector(".facebook-btn");
const twitterBtn = document.querySelector(".twitter-btn");
const linkedinBtn = document.querySelector(".linkedin-btn");
const whatsappBtn = document.querySelector(".whatsapp-btn");

function init() {
  let postUrl = encodeURI(document.location.href);
  let postTitle = encodeURI("Hi everyone, please check this out: ");
  let options = encodeURI('toolbar=0,status=0,resizable=1,width=626,height=436');

  facebookBtn.setAttribute(
    'onclick',
    `window.open('https://www.facebook.com/sharer.php?u=${postUrl}', 'sharer', '${options}')`
  );

  twitterBtn.setAttribute(
    'onclick',
    `window.open('https://twitter.com/share?url=${postUrl}&text=${postTitle}', 'sharer', '${options}')`
  );

  linkedinBtn.setAttribute(
    'onclick',
    `window.open('https://www.linkedin.com/shareArticle?url=${postUrl}&title=${postTitle}', 'sharer', '${options}')`
  );

  whatsappBtn.setAttribute(
    'onclick',
    `window.open('https://wa.me/?text=${postTitle} ${postUrl}', 'sharer', '${options}')`
  );

}

init();