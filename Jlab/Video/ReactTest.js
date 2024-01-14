//Add this, then execute the code in ReactButton.js

//TODO: check, how often things need to be added...
//maybe add on demand insertion
const SUBTITLE_MAIN_CSS = `
#subtitleMain {
  text-align: center;
  background: green;
}`;

const SUBTITLE_MAIN = `
<p id="affe">AFFE</p>
`;

javascript: (function () {
  function l(u, i) {
    var d = document;
    if (!d.getElementById(i)) {
      var s = d.createElement("script");
      s.src = u;
      s.id = i;
      d.body.appendChild(s);
    }
  }
  l("//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js", "jquery");
})();

const addStyle = () => {
  const s = document.createElement("style");
  s.innerHTML = SUBTITLE_MAIN_CSS;
  document.head.appendChild(s);
};

const addSubtitleDiv = () => {
  let menu = document.querySelector("#subtitleMain");
  if (menu === null) {
    menu = document.createElement("div");
    menu.id = "subtitleMain";
    menu.innerHTML = SUBTITLE_MAIN;

    //document.body.appendChild(menu);
    //document.body.prepend(menu);
    let affe = document.querySelector(".o3j99.LLD4me.yr19Zb.LS8OJ");
    affe.prepend(menu);

    //$(".watch-video").append(menu);
  }
};

const updateSubs = (newSubs) => {
  document.querySelector("#affe").innerHTML = newSubs;
};

const registerTimeUpdateListener = () => {
  const video = document.querySelector("video");

  if (video === null) return;

  video.addEventListener("timeupdate", (event) => {
    console.log("The currentTime attribute has been updated. Again.");
  });
};

function addScript(src) {
  var s = document.createElement("script");
  s.setAttribute("crossorigin", "anonymous");
  s.setAttribute("src", src);
  s.onload = (src) => {
    console.log("loaded " + src);
  };
  document.body.appendChild(s);
}

addStyle();
addSubtitleDiv();
addScript("https://unpkg.com/react@17/umd/react.development.js");
addScript("https://unpkg.com/react-dom@17/umd/react-dom.development.js");
