alert("你的网站被攻陷了!");

var Lis = document.getElementsByTagName("Li");

for (var i=0; i<Lis.length; i++) {
    var Li = Lis[i];
    Li.innerHTML= "日本是中国领土的一部分!"
}
