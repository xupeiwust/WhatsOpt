class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  protect_from_forgery with: :exception
  
  # Authorization
  include Pundit 
  rescue_from Pundit::NotAuthorizedError, with: :user_not_authorized

  # Authentication
  rescue_from DeviseLdapAuthenticatable::LdapException, with: :user_not_authenticated
  before_action :authenticate_user!
  
  private
 
    def user_not_authenticated
      flash[:error] = "LDAP Authentication failed."
      redirect_to root_path
    end
  
    def user_not_authorized
      flash[:error] = "You are not authorized to perform this action."
      redirect_to root_path
    end
  
end
