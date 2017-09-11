/**
 * Resize function without multiple trigger
 * 
 * Usage:
 * $(window).smartresize(function(){  
 *     // code here
 * });
 */
(function($,sr){
    // debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
  var debounce = function (func, threshold, execAsap) {
    var timeout;
      return function debounced () {
        var obj = this, args = arguments;
        function delayed () {
          if (!execAsap)
           func.apply(obj, args); 
          timeout = null; 
        }
        if (timeout)
          clearTimeout(timeout);
        else if (execAsap)
          func.apply(obj, args);
        timeout = setTimeout(delayed, threshold || 100); 
        };
    };

    // smartresize 
    jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };

})(jQuery,'smartresize');
/**
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var CURRENT_URL = window.location.href.split('#')[0].split('?')[0],
    $BODY = $('body'),
    $MENU_TOGGLE = $('#menu_toggle'),
    $SIDEBAR_MENU = $('#sidebar-menu'),
    $SIDEBAR_FOOTER = $('.sidebar-footer'),
    $LEFT_COL = $('.left_col'),
    $RIGHT_COL = $('.right_col'),
    $NAV_MENU = $('.nav_menu'),
    $FOOTER = $('footer');

// Sidebar
function init_sidebar() {
  var setContentHeight = function () {
    // reset height
    $RIGHT_COL.css('min-height', $(window).height());
    var bodyHeight = $BODY.outerHeight(),
    footerHeight = $BODY.hasClass('footer_fixed') ? -10 : $FOOTER.height(),
    leftColHeight = $LEFT_COL.eq(1).height() + $SIDEBAR_FOOTER.height(),
    contentHeight = bodyHeight < leftColHeight ? leftColHeight : bodyHeight;
    // normalize content
    contentHeight -= $NAV_MENU.height() + footerHeight;
    $RIGHT_COL.css('min-height', contentHeight);
    };
  
  $SIDEBAR_MENU.find('a').on('click', function(ev) {
    var $li = $(this).parent();

     if ($li.is('.active')) {
         $li.removeClass('active active-sm');
         $('ul:first', $li).slideUp(function() {
             setContentHeight();
         });
     } else {
         // prevent closing menu if we are on child menu
         if (!$li.parent().is('.child_menu')) {
             $SIDEBAR_MENU.find('li').removeClass('active active-sm');
             $SIDEBAR_MENU.find('li ul').slideUp();
         }else
         {
           if ( $BODY.is( ".nav-sm" ) )
           {
           $SIDEBAR_MENU.find( "li" ).removeClass( "active active-sm" );
           $SIDEBAR_MENU.find( "li ul" ).slideUp();
           }
           }
            $li.addClass('active');

            $('ul:first', $li).slideDown(function() {
                setContentHeight();
            });
        }
    });

// toggle small or large menu 
$MENU_TOGGLE.on('click', function() {
  if ($BODY.hasClass('nav-md')) {
    $SIDEBAR_MENU.find('li.active ul').hide();
    $SIDEBAR_MENU.find('li.active').addClass('active-sm').removeClass('active');
  } else {
    $SIDEBAR_MENU.find('li.active-sm ul').show();
    $SIDEBAR_MENU.find('li.active-sm').addClass('active').removeClass('active-sm');
  }
  $BODY.toggleClass('nav-md nav-sm');
  setContentHeight();
});
  // check active menu
  $SIDEBAR_MENU.find('a[href="' + CURRENT_URL + '"]').parent('li').addClass('current-page');
  
  $SIDEBAR_MENU.find('a').filter(function () {
  	return this.href == CURRENT_URL;
  }).parent('li').addClass('current-page').parents('ul').slideDown(function() {
  	setContentHeight();
  }).parent().addClass('active');
  
  // recompute content when resizing
  $(window).smartresize(function(){  
  	setContentHeight();
  });
  
  setContentHeight();
  
  // fixed sidebar
  if ($.fn.mCustomScrollbar) {
    $('.menu_fixed').mCustomScrollbar({
      autoHideScrollbar: true,
      theme: 'minimal',
      mouseWheel:{ preventDefault: true }
    });
  }
};
// /Sidebar

var randNum = function() {
 return (Math.floor(Math.random() * (1 + 40 - 20))) + 20;
};


// Tooltip
$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip({
        container: 'body'
    });
});
// /Tooltip


// iCheck
$(document).ready(function() {
 if ($("input.flat")[0]) {
   $(document).ready(function () {
     $('input.flat').iCheck({
       checkboxClass: 'icheckbox_flat-green',
       radioClass: 'iradio_flat-green'
     });
   });
 }
});
// /iCheck

// Table
$('table input').on('ifChecked', function () {
    checkState = '';
    $(this).parent().parent().parent().addClass('selected');
    countChecked();
});
$('table input').on('ifUnchecked', function () {
    checkState = '';
    $(this).parent().parent().parent().removeClass('selected');
    countChecked();
});

var checkState = '';

$('.bulk_action input').on('ifChecked', function () {
    checkState = '';
    $(this).parent().parent().parent().addClass('selected');
    countChecked();
});
$('.bulk_action input').on('ifUnchecked', function () {
    checkState = '';
    $(this).parent().parent().parent().removeClass('selected');
    countChecked();
});
$('.bulk_action input#check-all').on('ifChecked', function () {
    checkState = 'all';
    countChecked();
});
$('.bulk_action input#check-all').on('ifUnchecked', function () {
    checkState = 'none';
    countChecked();
});

function countChecked() {
    if (checkState === 'all') {
        $(".bulk_action input[name='table_records']").iCheck('check');
    }
    if (checkState === 'none') {
        $(".bulk_action input[name='table_records']").iCheck('uncheck');
    }

    var checkCount = $(".bulk_action input[name='table_records']:checked").length;

    if (checkCount) {
        $('.column-title').hide();
        $('.bulk-actions').show();
        $('.action-cnt').html(checkCount + ' Records Selected');
    } else {
        $('.column-title').show();
        $('.bulk-actions').hide();
    }
}
	   
/* AUTOSIZE */
			
function init_autosize() {
  if(typeof $.fn.autosize !== 'undefined'){
    autosize($('.resizable_textarea'));
  }
};  
   
/* DATA TABLES */
			
function init_DataTables() {
  if( typeof ($.fn.DataTable) === 'undefined'){ return; }
  var handleDataTableButtons = function() {
    if ($("#datatable-buttons").length) {
      $("#datatable-buttons").DataTable({
        dom: "Bfrtip",
        buttons: [
      	{
      	  extend: "copy",
      	  className: "btn-sm"
      	},
      	{
      	  extend: "csv",
      	  className: "btn-sm"
      	},
      	{
      	  extend: "excel",
      	  className: "btn-sm"
      	},
      	{
      	  extend: "pdfHtml5",
      	  className: "btn-sm"
      	},
      	{
      	  extend: "print",
      	  className: "btn-sm"
      	},
        ],
        responsive: true
    });
      }
    };
    
  TableManageButtons = function() {
    "use strict";
    return {
          init: function() {
            handleDataTableButtons();
          }
    };
  }();

  $('#datatable').dataTable();
  
  $('#datatable-keytable').DataTable({
    keys: true
  });
  
  $('#datatable-responsive').DataTable();
  
  $('#datatable-scroller').DataTable({
    ajax: "js/datatables/json/scroller-demo.json",
    deferRender: true,
    scrollY: 380,
    scrollCollapse: true,
    scroller: true
  });
  
  $('#datatable-fixed-header').DataTable({
    fixedHeader: true
  });
  
  var $datatable = $('#datatable-checkbox');
  
  $datatable.dataTable({
    'order': [[ 1, 'asc' ]],
    'columnDefs': [
  	{ orderable: false, targets: [0] }
    ]
  });
  $datatable.on('draw.dt', function() {
    $('checkbox input').iCheck({
  	checkboxClass: 'icheckbox_flat-green'
    });
  });
  
  TableManageButtons.init();
	
};

$(document).ready(function() {
        init_sidebar();
	init_DataTables();
	init_autosize();
});	
