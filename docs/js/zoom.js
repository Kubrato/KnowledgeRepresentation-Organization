/* Click-to-zoom for figures marked with class="zoomable".
   Click the image to enlarge it in place; click again to shrink it back.
   No full-screen view is opened. */

document.addEventListener("DOMContentLoaded", function () {
  var thumbs = document.querySelectorAll("img.zoomable");

  for (var i = 0; i < thumbs.length; i++) {
    setupZoom(thumbs[i]);
  }

  function setupZoom(img) {
    // Wrap the image so the icon can sit on top of it.
    var wrap = document.createElement("span");
    wrap.className = "zoom-wrap";
    img.parentNode.insertBefore(wrap, img);
    wrap.appendChild(img);

    // A small magnifying-glass icon so people see the image can be zoomed.
    var badge = document.createElement("span");
    badge.className = "zoom-badge";
    badge.textContent = "🔍";
    wrap.appendChild(badge);

    // Toggle the enlarged state on click.
    img.addEventListener("click", function () {
      img.classList.toggle("zoomed");
    });
  }
});
