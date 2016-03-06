(function($, Backbone, _, app) {
  var TemplateView = Backbone.View.extend({
    templateName: '',
    initialize: function() {
      this.template = _.template($(this.templateName).html());
    },
    render: function() {
      var context = this.getContext(),
          html = this.template(context);
      this.$el.html(html);
    },
    getContext: function() {
      return {};
    }
  });

  var FormView = TemplateView.extend({
    events: {
      'submit form': 'submit'
    },
    errorTemplate: _.template('<span class="help-block error"><%- msg %></span>'),
    clearErrors: function() {
      $('.error', this.form).remove();
      $('.form-group', this.form).removeClass('has-error');
    },
    showErrors: function(errors) {
      _.map(errors, function (fieldErrors, name) {
        var $field = $(':input[name=' + name + ']', this.form),
            $formGroup = $field.closest('.form-group'),
            $inputGroup = $field.parent();
        if ($inputGroup.hasClass('input-group'))
          $inputGroup.after(this.errorTemplate({msg: fieldErrors}));
        else
          $field.after(this.errorTemplate({msg: fieldErrors}));
        $formGroup.addClass('has-error');
      }, this);
    },
    serializeForm: function(form) {
      return _.object(_.map(form.serializeArray(), function(item) {
        // Convert object to tuple of (name, value)
        return [item.name, item.value];
      }));
    },
    submit: function(event) {
      event.preventDefault();
      this.form = $(event.currentTarget);
      this.clearErrors();
    },
    failure: function(xhr, status, error) {
      var errors = xhr.responseJSON;
      this.showErrors(errors);
    },
    done: function(event) {
      if (event) {
        event.preventDefault();
      }
      this.trigger('done');
      this.remove();
    },
    modelFailure: function(model, xhr, options) {
      var errors = xhr.responseJSON;
      this.showErrors(errors);
    }
  });

  var HomepageView = TemplateView.extend({
    templateName: '#home-template',
    initialize: function(options) {
      this.on('rendered', this.rendered);
      var self = this;
      TemplateView.prototype.initialize.apply(this, arguments);
      $.get(app.apiMe, function(user) {
        app.me = user;
        $.proxy(self.render, self)();
        var clipboard = new Clipboard('.btn-copy', {
          text: function(trigger) {
            return user.shareable_link;
          }
        }); 
      });
    },
    getContext: function() {
      return {me: app.me || null};
    }
  });

  var LoginView = FormView.extend({
    id: 'login',
    templateName: '#login-template',
    events: {
      'submit form.form-login': 'submit'
    },
    submit: function(event) {
      var data = {};
      FormView.prototype.submit.apply(this, arguments);
      data = this.serializeForm(this.form);
      $.post(app.apiLogin, data)
        .success($.proxy(this.loginSuccess, this))
        .fail($.proxy(this.failure, this));
    },
    loginSuccess: function(data) {
      app.session.save(data.token);
      this.done();
    },
    render: function() {
      FormView.prototype.render.apply(this, arguments);
      var newUser = new NewUserView();
      $('#tab-register').append(newUser.el);
      newUser.render();
    },
    done: function(event) {
      if (event) {
        event.preventDefault();
      }
      this.trigger('done');
      $('#login').remove();
    },
  });

  var NewUserView = FormView.extend({
    className: 'new-user',
    templateName: '#new-user-template',
    events: {
      'submit form.form-new-user': 'submit'
    },
    submit: function(event) {
      var self = this,
          attributes = {};
      FormView.prototype.submit.apply(this, arguments);
      attributes = this.serializeForm(this.form);
      app.collections.ready.done(function() {
        app.users.create(attributes, {
          wait: true,
          success: $.proxy(self.success, self),
          error: $.proxy(self.modelFailure, self)
        });
      });
    },
    success: function(model) {
      $('.form-login [name="username"]').val(model.attributes.username);
      $('.form-login [name="password"]').val(model.attributes.password);
      $('.form-login').trigger('submit');
    }
  });

  var HeaderView = TemplateView.extend({
    tagName: 'header',
    templateName: '#header-template',
    events: {
      'click a.logout': 'logout'
    },
    getContext: function() {
      return {authenticated: app.session.authenticated()};
    },
    logout: function(event) {
      event.preventDefault();
      app.session.delete();
      window.location = '/';
    }
  });

  var CommissionListView = TemplateView.extend({
    templateName: '#commission-list-template',
    initialize: function(options) {
      var self = this;
      TemplateView.prototype.initialize.apply(this, arguments);
      app.collections.ready.done(function() {
        app.commissionDetails.fetch({
          success: $.proxy(self.render, self)
        });
      });
    },
    getContext: function () {
      return {commissionDetails: app.commissionDetails || null};
    }
  });

  app.views.HomepageView = HomepageView;
  app.views.LoginView = LoginView;
  app.views.NewUserView = NewUserView;
  app.views.HeaderView = HeaderView;
  app.views.CommissionListView = CommissionListView;

})(jQuery, Backbone, _, app)