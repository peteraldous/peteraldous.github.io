// lib Maybe 
var Maybe = {} ;

/* Helper functions for obscuring email. 

   Most spam-crawlers don't seem to use javascript. */

Maybe.emailme = function (text) {
  var a='a';
  if (!text) text = a + 'l' + 'd' + 'ou' + 's' + '@cs.b' + 'y' + 'u.ed' + 'u' ;
  document.write('<' + a + ' href="m' + a + 'i'+'lto:'+a+'ldo' + 'us' + '@c'+'s.by' + 'u.ed'+'u">'+text+'</a>');
} ;

Maybe.email = function (account,domain,text) {
  document.write('<a href="mailto:'+account+'@'+domain+'">'+text+'</a>') ;
} ;
