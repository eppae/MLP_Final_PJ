import { rovingIndex } from 'https://cdn.skypack.dev/roving-ux' // cdn es2020

document.querySelectorAll('.horizontal-media-scroller')
  .forEach(scroller => rovingIndex({
    element: scroller,
    target: 'a',
  }))