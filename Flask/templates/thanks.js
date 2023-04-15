image_arry = [
  'malone.gif'
  'omg-thank-you.gif'
  'thank1.gif'
  'thank2.gif'
  'thankyou_cat.gif'
  ]

function get_random_image(){
 random_index = Math.floor(Math.random() * image_array.length);
  
  selected_iamge = image_array(random_index]
                               
  document.getElementByID('image_shower').src = './pictures/${selected_image}'                              
}
