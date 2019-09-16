odoo.define('bus.demo', function(require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var Widget = require('web.Widget');
    var _t = core._t;
    var WebClient = require('web.WebClient');
    var session = require('web.session');
    var QWeb = core.qweb;

    var busAction = AbstractAction.extend({
        template: "bus_template",
        start: function() {
            this._super.apply(this, arguments);
            var bus = new Bus(this);
            bus.appendTo(this.$('#open'));;
        },
    });

    var busstAction = AbstractAction.extend({
        template: "busst_template",
        init: function(parent) {
            this._super(parent);
            this.call('bus_service', 'startPolling');
        },
        start: function() {
            this._super.apply(this, arguments);
            var busst = new Bus_st(this);
            busst.appendTo(this.$('#close'));
        },
    });

    var Bus = Widget.extend({
        template: 'busdemo_widget',
        events: {
            'click .submit': '_onClickSubmit',
        },
        _onClickSubmit: function() {
            
            var data = this.$('.quantity').val();
            var domain = [['name', '=', data]];
            var self = this;
            return self._rpc({
                    model: 'bus.demo',
                    method: 'search_read',
                    args: [domain],
                    fields: ['name', 'image'],
                }).then(function(result) {
                    if (result.length) {
                        return self._rpc({
                                model: 'bus.demo',
                                method: 'notify_student',
                                args: result
                            }).then(function(result) {
                                self.do_notify(_t("Success"), _t("Your data is submitted"));
                                self.$('.quantity').val("");
                            });
                    } else {
                        self.do_notify(_t("Failure"), _t("Your data is not submitted"));
                    }
                });
        },
    });

    var Bus_st = Widget.extend({
        template: 'busdemost_widget',
        events: {
            'click .ok': '_onClickOk',
            'click .join': '_onClickJoin',
        },
        init: function(parent) {
            this._super(parent);
            console.log("!!!!!!!!!!!!!!!!!!!!!!",session.partner_id);
            this.image = "";
            core.bus.on('display_img', this, this._onImageDisplay);
        },
        willStart: function () {
            var self = this;
            var domain = [['partner_id', '=', session.partner_id]];
                return this._rpc({
                        model: 'busdemo.student',
                        method: 'search_read',
                        args: [domain],
                })
            .then(function (result) {
                console.log("=================",result);
                self.studentdata = result;
            }); 
        },
        start: function () {
            if(this.studentdata.partner_id != null){
                this.$el.html(QWeb.render('busdemost_widget', {
                    studentdata: this.studentdata,
                }));
            }
            else{
               this.$el.html(QWeb.render('busdemost_widget', {
                    studentdata: false,
                })); 
            }
            return this._super.apply(this, arguments);
        },
        _onImageDisplay: function(imgData) {
            this.image = imgData
            this.$el.html(QWeb.render('busdemost_widget', {
                img:imgData,
                studentdata: this.studentdata,
            }));
        },
        _onClickOk: function() {
            var val = this.$(".quality").val();
            if (this.image.name == val) {
                this.do_notify(_t("Success"), _t("Correct Answer"));
                this.$(".quality").val("");
            } else {
                this.do_warn(_t("Error"), _t("Incorrect Answer"));

            }
        },
        _onClickJoin: function(imgData) {
            this.do_notify(_t("Success"), _t("Thank you for joinning"));

            this.$el.html(QWeb.render('busdemost_widget', {
                studentdata: this.studentdata,
                // img:imgData,
            }));
            return this._rpc({
                route: '/teacher/',
                params: {
                    partner_id: session.partner_id,
                },
            })
        },
    });

    // Receive Notification
    WebClient.include({
        image_display: function(img){
            if(typeof(img)!=undefined){
                core.bus.trigger('display_img', img);
            }
        },
        show_application: function() {
            this.call('bus_service', 'onNotification', this, function(notifications) {
                console.log(notifications)
                _.each(notifications, (function(notification) {
                    if (notification[0][1] === 'image.data') {
                        this.image_display(notification[1]);
                    }
                }).bind(this));
            });
            return this._super.apply(this, arguments);
        },
    });

    core.action_registry.add('bsexample', busAction);
    core.action_registry.add('bsexamplest', busstAction);
    return busAction, busstAction;

});