window.addEventListener("load", () => {
  let orientation =
    (screen.orientation || {}).type ||
    screen.mozOrientation ||
    screen.msOrientation;
  console.log("hello");
  //   $("#id_check_in").datepicker({
  //     language: "en",
  //     autoClose: true,
  //     minDate: new Date(),
  //     dateFormat: "yyyy-mm-dd",
  //     position:
  //       typeof window.orientation !== "undefined"
  //         ? "top center"
  //         : "bottom center",
  //     range: true,
  //     multipleDatesSeparator: "/",
  //   });
  $("#id_check_in").datepicker({
    language: "en",
    autoClose: true,
    minDate: new Date(),
    dateFormat: "yyyy-mm-dd",
    // timeFormat: 'hh:ii',
    // timepicker: true,
    // dateTimeSeparator: ' ',
    position:
    orientation === "portrait-secondary" || orientation === "portrait-primary"
        ? "top center"
        : "bottom center",
    // range: true,
    // multipleDatesSeparator: "/",
  });
  $("#id_check_out").datepicker({
    language: "en",
    autoClose: true,
    minDate: new Date(),
    dateFormat: "yyyy-mm-dd",
    // timeFormat: "hh:mm",
    // timepicker: true,
    // dateTimeSeparator: " ",
    position:
      orientation === "portrait-secondary" || orientation === "portrait-primary"
        ? "top center"
        : "bottom center",
    // range: true,
    // multipleDatesSeparator: "/",
  });
});
