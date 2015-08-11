// lib Maybe 
var Maybe = {} ;

/* Helper functions for obscuring email. 

   Most spam-crawlers don't seem to use javascript. */

Maybe.emailme = function (text) {
  var a='a';
  if (!text) text = 'pet' + 'e' + 'y' + a + '@cs.u' + 't' + a + 'h.ed' + 'u' ;
  document.write('<' + a + ' href="m' + a + 'i'+'lto:'+'p'+'etey' + a + '@c'+'s.ut' + a + 'h.ed'+'u">'+text+'</a>');
} ;

Maybe.email = function (account,domain,text) {
  document.write('<a href="mailto:'+account+'@'+domain+'">'+text+'</a>') ;
} ;

Maybe.descriptions = ['I climb Mount Everest every other weekend.',
                      "I'm kind of a big deal.",
					  "You might think it's a halo, but it's really just my bald head shining.",
					  "I'm basically Bruce Schneier. Except he has hair.",
                      "If I'm not in my lab, I'm probably out saving the world."];

Maybe.generateDescription = function () {
  document.write('<p>' + Maybe.descriptions[Math.floor(Math.random()*Maybe.descriptions.length)] + '</p>');
} ;
