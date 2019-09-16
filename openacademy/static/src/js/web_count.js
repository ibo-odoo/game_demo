odoo.define('openacademy.web_count', function (require) {
"use strict";

var core = require('web.core');
var AbstractAction = require('web.AbstractAction');
var Widget = require('web.Widget');
var SystrayMenu = require('web.SystrayMenu');


var openAction=AbstractAction.extend({
      template: "counter_template",
      events:{
          'click .add':'_onClickAddwidget'
      },
     start: function(){
          this._super.apply(this, arguments);
          this._onClickAddwidget()
      },
    _onClickAddwidget: function(){
          var counter = new Counter(this, 0);
          counter.appendTo(this.$el.find('#open'));
    },
});

var Counter = Widget.extend({
    template: 'counter_widget',
    events: {
        'click .increment': '_onClickIncrement',
        'click .decrement': '_onClickDecrement',
        'click .delete': '_onClickDelete',

    },
    init: function (parent, value) {
        this._super(parent);
        this.count = value;
    },
    start: function(){
        this.$('.quantity').val(this.count);
     },
    _onClickIncrement: function () {
        this.count++;
        this.$('.quantity').val(this.count);
        //this.do_notify(_t("Increase"), _t("Your number is increased"));
    },
    _onClickDecrement: function () {
        this.count--;
        this.$('.quantity').val(this.count);
        //this.do_notify(_t("Decrease"), _t("Your number is decreased"));
    },
    _onClickDelete: function () {
        //this.do_warn(_t("Error"), _t("Dont delete this"));
        this.destroy();
    },
});
   
core.action_registry.add('counter_a', openAction);
return openAction;

});
