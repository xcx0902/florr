// ==UserScript==
// @name florr
// @namespace Violentmonkey Scripts
// @match https://florr.io/
// @grant none
// @version 1.0.edited
// @author xcx0902
// ==/UserScript==

for (const {prototype} of [OffscreenCanvasRenderingContext2D, CanvasRenderingContext2D]) {
  prototype.arc = function (x, y, r) {
    this.rect(x - r, y - r, r * 2, r * 2);
  }
  prototype.ellipse = function (x, y, w, h) {
    this.rect(x - w, y - h, w * 2, h * 2);
  }
}
