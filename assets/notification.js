/*
 * Notification js
 * https://amaterasusan.github.io/notification
 * @license MIT licensed
 *
 * Copyright (C) 2024 Helen Nikitina
 */
function Notification(options = {}) {
  let opts = {};
  let timeouts = {};
  const defNumberOpened = 5;
  const defMaxNumberOpened = 10;
  const defDuration = 5000;
  const allowedPosition = ['top-right', 'bottom-right', 'top-left', 'bottom-left', 'center'];
  const defaultOpts = {
    position: 'top-right',
    duration: defDuration,
    isHidePrev: false,
    isHideTitle: false,
    maxOpened: defNumberOpened,
  };

  const setProperty = (obj = {}) => {
    const defOpts = Object.keys(opts).length ? opts : defaultOpts;
    opts = !!obj && obj.constructor.name === 'Object' ? Object.assign({}, defOpts, obj) : defOpts;
    // check position
    if (!allowedPosition.includes(opts.position)) {
      opts.position = allowedPosition[0];
    }
    // check duration
    opts.duration = parseInt(opts.duration);
    if (isNaN(opts.duration) || (opts.duration < 1000 && opts.duration !== 0)) {
      opts.duration = defDuration;
    }
    // check maxOpened
    opts.maxOpened = parseInt(opts.maxOpened);
    if (isNaN(opts.maxOpened) || opts.maxOpened < 1 || opts.maxOpened > defMaxNumberOpened) {
      opts.maxOpened = defNumberOpened;
    }
  };

  setProperty(options);

  // selectors
  const classContainer = 'notification-container';
  const classPopup = 'notification';
  const animationInClass = 'animation-slide-in';
  const animationOutClass = 'animation-slide-out';
  const animationFadeInClass = 'animation-fade-in';
  const animationFadeOutClass = 'animation-fade-out';
  const titleTextSel = '.notification-title .title';
  const descSel = '.notification-desc';
  const closeSel = '.notification-close';
  const actionButSel = '.notification-action';
  const cancelButSel = '.notification-cancel';
  const overlayClass = 'overlay';

  // class, defaultTitle and defaultMessage
  const dataByType = {
    dialog: {
      classType: 'notification-dialog',
      defaultTitle: 'Confirm',
      defaultMessage: 'Default Confirm message',
    },
    info: {
      classType: 'notification-info',
      defaultTitle: 'Info',
      defaultMessage: 'default Info',
    },
    success: {
      classType: 'notification-success',
      defaultTitle: 'Success',
      defaultMessage: 'default Success',
    },
    warning: {
      classType: 'notification-warning',
      defaultTitle: 'Warning',
      defaultMessage: 'default Warning',
    },
    error: {
      classType: 'notification-error',
      defaultTitle: 'Error',
      defaultMessage: 'An error has occurred',
    },
  };

  const dialogButtons = () => {
    return `<div class="notification-buttons">
    <span class="notification-button notification-cancel"></span>
    <span class="notification-button notification-action"></span>
    </div>`;
  };

  const createOverlay = () => {
    if (!document.querySelector(`.${overlayClass}`)) {
      const overlayEl = document.createElement('div');
      overlayEl.classList.add(overlayClass);
      document.body.appendChild(overlayEl);
    }
    document.querySelector(`.${overlayClass}`).classList.add('active');
  };

  // Type-specific SVG icons (16x16, Bootstrap-style)
  const typeIcons = {
    error: '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/><path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/></svg>',
    success: '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/><path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05"/></svg>',
    warning: '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/></svg>',
    info: '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/><path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/></svg>',
    dialog: '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/><path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286m1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94"/></svg>'
  };

  const tempatePopup = (type) => {
    const icon = typeIcons[type] || typeIcons.info;
    const closeEl = '<button type="button" class="notification-close" aria-label="Close"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/></svg></button>';

    const titleBlock = opts.isHideTitle ? '' :
      '<div class="notification-title">' +
        '<div class="notif-icon-wrap">' + icon + '</div>' +
        '<div class="title"></div>' +
        closeEl +
      '</div>';

    const progressBar = (opts.duration && opts.duration > 0 && type !== 'dialog')
      ? '<div class="notification-progress"><div class="notification-progress-bar"></div></div>'
      : '';

    return titleBlock +
      '<div class="notification-body">' +
        '<div class="notification-desc"></div>' +
        (opts.isHideTitle && opts.duration === 0 && type !== 'dialog' ? closeEl : '') +
      '</div>' +
      progressBar +
      (type === 'dialog' ? dialogButtons() : '');
  };

  const createMainContainer = () => {
    let container = document.querySelector(`.${classContainer}.${opts.position}`);

    if (!container) {
      container = document.createElement('div');
      container.classList = `${classContainer} ${opts.position}`;
      document.body.appendChild(container);
    }

    return container;
  };

  const createPopup = (type) => {
    const container = createMainContainer();
    if (container.childElementCount >= opts.maxOpened) {
      if (opts.position.includes('bottom')) {
        hidePopUp(container.lastChild);
      } else {
        hidePopUp(container.firstChild);
      }
    }

    const elPopup = document.createElement('div');
    elPopup.classList.add(
      classPopup,
      opts.position === 'center' ? animationFadeInClass : animationInClass,
      dataByType[type].classType
    );
    elPopup.dataset.type = type;
    elPopup.dataset.position = opts.position;
    elPopup.dataset.id = new Date().getTime();

    // insert template in element
    elPopup.insertAdjacentHTML('beforeend', tempatePopup(type));

    // Set progress bar animation duration
    if (opts.duration && opts.duration > 0 && type !== 'dialog') {
      var bar = elPopup.querySelector('.notification-progress-bar');
      if (bar) bar.style.animationDuration = opts.duration + 'ms';
    }

    // create overlay
    if (type === 'dialog') {
      createOverlay();
    }

    // add element to container in the required sequence
    if (opts.position.includes('bottom')) {
      container.prepend(elPopup);
    } else {
      container.appendChild(elPopup);
    }

    return elPopup;
  };

  const showPopup = ({ type, title, message, callback = null, validFunc = null } = {}) => {
    if (opts.isHidePrev) {
      hide();
    }

    const elPopup = createPopup(type);

    // set title and message
    const elTitle = elPopup.querySelector(titleTextSel);
    const elText = elPopup.querySelector(descSel);
    if (elTitle) {
      elTitle.innerHTML = title || dataByType[type].defaultTitle;
    }
    elText.innerHTML = message || dataByType[type].defaultMessage;

    if (type === 'dialog') {
      // set buttons click event
      setButtonsEvent(elPopup, callback, validFunc);
    } else if (opts.duration) {
      // store new timeout to timeouts obj if type is not dialog
      const timeout = setTimeout(() => hidePopUp(elPopup), opts.duration);
      timeouts[elPopup.dataset.id] = timeout;
    }

    // add click event to close element
    setCloseEvent(elPopup);
  };

  const setButtonsEvent = (elPopup, callback = null, validFunc = null) => {
    const elAction = elPopup.querySelector(actionButSel);
    elAction?.addEventListener(
      'click',
      function handlerAction(event) {
        event.stopPropagation();
        event.preventDefault();
        let valid = true;
        if (validFunc) {
          valid = validFunc();
        }
        if (!valid) {
          return false;
        }
        hidePopUp(elPopup);

        elAction.removeEventListener('click', handlerAction, false);
        if (callback) {
          return callback('ok');
        }
        return false;
      },
      false
    );

    const elCancel = elPopup.querySelector(cancelButSel);
    elCancel?.addEventListener(
      'click',
      function handlerCancel(event) {
        event.stopPropagation();
        event.preventDefault();
        hidePopUp(elPopup);

        elCancel.removeEventListener('click', handlerCancel, false);
        if (callback) {
          return callback('cancel');
        }
        return false;
      },
      false
    );
  };

  const setCloseEvent = (elPopup) => {
    const elClose = elPopup.querySelector(closeSel);
    elClose?.addEventListener(
      'click',
      function handlerClose() {
        hidePopUp(elPopup);
        elClose.removeEventListener('click', handlerClose, false);
      },
      false
    );
  };

  const hidePopUp = (elPopup) => {
    const container = document.querySelector(`.${classContainer}.${elPopup.dataset.position}`);

    clearTimeout(timeouts[elPopup.dataset.id]);
    delete timeouts[elPopup.dataset.id];

    // change animation class
    elPopup.classList.remove(elPopup.dataset.position === 'center' ? animationFadeInClass : animationInClass);
    elPopup.classList.add(elPopup.dataset.position === 'center' ? animationFadeOutClass : animationOutClass);

    if (elPopup.dataset.type === 'dialog') {
      document.querySelector(`.${overlayClass}`)?.classList.remove('active');
    }

    setTimeout(function () {
      if (elPopup.parentNode === container) {
        container.removeChild(elPopup);
      }

      // Remove container if it empty
      if (!container?.hasChildNodes() && container?.parentElement === document.body) {
        document.body.removeChild(container);
      }
    }, 400);
  };

  const hide = () => {
    const containers = document.querySelectorAll(`.${classContainer}`);
    document.querySelector(`.${overlayClass}`)?.classList.remove('active');

    for (const key in timeouts) {
      clearTimeout(timeouts[key]);
    }
    timeouts = {};

    containers.forEach((container) => {
      if (container && container.parentElement === document.body) {
        document.body.removeChild(container);
      }
    });
  };

  const dialog = ({ title, message, callback = null, validFunc = null }) =>
    showPopup({ type: 'dialog', title, message, callback, validFunc });
  const info = ({ title, message }) => showPopup({ type: 'info', title, message });
  const success = ({ title, message }) => showPopup({ type: 'success', title, message });
  const warning = ({ title, message }) => showPopup({ type: 'warning', title, message });
  const error = ({ title, message }) => showPopup({ type: 'error', title, message });
  return { dialog, info, success, warning, error, setProperty, hide };
}
