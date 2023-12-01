function calculateSettingAsThemeString({ localStorageTheme, systemSettingDark }) {
  if (localStorageTheme !== null) {
    return localStorageTheme;
  }

  // window.matchMedia('(prefers-color-scheme:dark)').matches가 true일때.
  if (systemSettingDark.matches) {
    return "dark";
  }

  // localStorageTheme이 light가 초기.
  return "light";
}

// Utility function to update the button text and aria-label. + icon
function updateButton({ buttonEl, isDark }) {
  const modeIcon = document.querySelector('#darkmodeIcon')
  const modeText = document.querySelector('.darkmode-text')
  const newCta = isDark ? "light" : "dark";
  const newText = isDark ? " LIGHTMODE" : " DARKMODE";
  modeText.innerHTML = newText
  buttonEl.setAttribute("aria-label", newCta);
  const newSrc = isDark ? darkIconURL : lightIconURL;
  modeIcon.src = newSrc;
}

//Utility function to update the theme setting on the html tag
function updateThemeOnHtmlEl({ theme }) {
  document.querySelector("html").setAttribute("data-theme", theme);
}


// Page

/**
* 1. Grab what we need from the DOM and system settings on page load
*/
const buttonForDarkMode = document.querySelector("[data-theme-toggle]");
const localStorageTheme = localStorage.getItem("theme");
const systemSettingDark = window.matchMedia("(prefers-color-scheme: dark)");

/**
* 2. Work out the current site settings
*/
let currentThemeSetting = calculateSettingAsThemeString({ localStorageTheme, systemSettingDark });

/**
* 3. Update the theme setting and button text accoridng to current settings
*/
updateButton({ buttonEl: buttonForDarkMode, isDark: currentThemeSetting === "dark" });
updateThemeOnHtmlEl({ theme: currentThemeSetting });

/**
* 4. Add an event listener to toggle the theme
*/
buttonForDarkMode.addEventListener("click", (event) => {
  const newTheme = currentThemeSetting === "dark" ? "light" : "dark"; // dark이면 light로 바꿀 수 있게.

  localStorage.setItem("theme", newTheme);
  updateButton({ buttonEl: buttonForDarkMode, isDark: newTheme === "dark" });
  updateThemeOnHtmlEl({ theme: newTheme });

  currentThemeSetting = newTheme;
}); 