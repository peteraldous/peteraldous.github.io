// lib Maybe 
var Maybe = {} ;

/* Helper functions for obscuring email. 

   Most spam-crawlers don't seem to use javascript. */

Maybe.emailme = function (text) {
  var a='a';
  if (!text) text = 'p' + a + 'l' + 'd' + 'ou' + 's' + '@gra' + 'm' + 'mat' + 'ech.' + 'com' ;
  document.write('<' + a + ' href="m' + a + 'i'+'lto:p'+a+'ldo' + 'us' + '@gr'+'amm' + 'ate'+'ch.com">'+text+'</a>');
} ;

Maybe.email = function (account,domain,text) {
  document.write('<a href="mailto:'+account+'@'+domain+'">'+text+'</a>') ;
} ;
