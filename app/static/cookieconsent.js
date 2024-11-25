window.addEventListener("load",function(){
    window.cookieconsent.initialise({
      palette:{
          popup:{
            background: "#e0e0e0",
            text: "#000000"
          },
          button:{
            background: "#0000CC",
             text: "#ffffff"
          }
        },
        content: {
          message: "This website uses cookies!",
          dismiss: "Okay"
        }
    })});