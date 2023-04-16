
  window.onload = choosePic;

  var myPix = new Array(  'pictures/malone.gif',
  'pictures/omg-thank-you.gif',
  'pictures/thank1.gif',
  'pictures/thank2.gif',
  'pictures/thankyou_cat.gif');
  
  function choosePic() {
       var randomNum = Math.floor(Math.random() * myPix.length);
       document.getElementById("image_shower").src = myPix[randomNum]}
