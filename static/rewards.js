/*
 jQuery animateNumber plugin v0.0.10
 (c) 2013, Alexandr Borisov.
 https://github.com/aishek/jquery-animateNumber
*/
(function(d){var p=function(b){return b.split("").reverse().join("")},l={numberStep:function(b,a){var e=Math.floor(b);d(a.elem).text(e)}},h=function(b){var a=b.elem;a.nodeType&&a.parentNode&&(a=a._animateNumberSetter,a||(a=l.numberStep),a(b.now,b))};d.Tween&&d.Tween.propHooks?d.Tween.propHooks.number={set:h}:d.fx.step.number=h;d.animateNumber={numberStepFactories:{append:function(b){return function(a,e){var k=Math.floor(a);d(e.elem).prop("number",a).text(k+b)}},separator:function(b,a){b=b||" ";a=
a||3;return function(e,k){var c=Math.floor(e).toString(),s=d(k.elem);if(c.length>a){for(var f=c,g=a,l=f.split("").reverse(),c=[],m,q,n,r=0,h=Math.ceil(f.length/g);r<h;r++){m="";for(n=0;n<g;n++){q=r*g+n;if(q===f.length)break;m+=l[q]}c.push(m)}f=c.length-1;g=p(c[f]);c[f]=p(parseInt(g,10).toString());c=c.join(b);c=p(c)}s.prop("number",e).text(c)}}}};d.fn.animateNumber=function(){for(var b=arguments[0],a=d.extend({},l,b),e=d(this),k=[a],c=1,h=arguments.length;c<h;c++)k.push(arguments[c]);if(b.numberStep){var f=
this.each(function(){this._animateNumberSetter=b.numberStep}),g=a.complete;a.complete=function(){f.each(function(){delete this._animateNumberSetter});g&&g.apply(this,arguments)}}return e.animate.apply(e,k)}})(jQuery);

/* App */
$(document).ready(function(){

    var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
    $('[data-animate="count-out"]').each(function(){
      thisValue = $(this).data('value');
      $(this).animateNumber({ number: thisValue, numberStep: comma_separator_number_step });
    });

    $('[data-toggle="popover"]').popover();

    //Animate Color Scales
    $('[data-animate="colorScale"]').each(function(){
      thisValue = $(this).data('value');
      $(this).find('.scoreTick, .scoreArrow').css("left", thisValue+"%");
    });

    var Donutoptions = {
        segmentShowStroke : false,
        animation: true,
        animationEasing: 'linear',
        animationSteps: '20',
        onAnimationComplete: function()
          {
              this.showTooltip(this.segments, true);  
          },
        tooltipEvents: [],
        showTooltips: true,
        tooltipTemplate: "<%if (label){%><%=label%>: <%}%>$<%= value %>",
        tooltipFillColor: "#404040",
        tooltipFontFamily: "'Open Sans',Helvetica,Arial, sans-serif"
    };

    $('[data-chart="doughnut"]').each(function(){
      var ct = $(this).get(0).getContext('2d');
      newChart = new Chart(ct).Doughnut(window["data"+$(this).get(0).id], Donutoptions);
    });
});