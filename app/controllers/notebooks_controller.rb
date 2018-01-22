class NotebooksController < ApplicationController
  before_action :set_notebook, only: [:show, :edit, :update, :destroy]
    
  # GET /notebooks
  def index
    @notebooks = Notebook.all
  end
  
  # GET /notebooks/1
  def show
  end

  # GET /notebooks/new
  def new
    @notebook = Notebook.new
  end
  
  # GET /notebooks/1/edit
  def edit
  end
  
  # POST /notebooks
  def create
    if params[:cancel_button]
      redirect_to notebooks_url, notice: "Notebook creation cancelled."
    else 
      @notebook = Notebook.create(notebook_params)
      if @notebook.save
        current_user.add_role(:owner, @notebook)
        current_user.save
        redirect_to notebook_url(@notebook), notice: "Notebook was successfully created."
      else
        flash[:error] = "Notebook creation failed: invalid input data."
        render :action => 'new'
      end
    end
  end
  
  # PATCH/PUT /notebooks/1
  def update
    authorize @notebook
    if @notebook.update(notebook_params)
      flash[:notice] = "Successfully updated notebook."
      redirect_to notebook_url
    else
      render :action => 'edit'
    end
  end
  
  # DELETE /notebooks/1
  def destroy
    authorize @notebook
    @notebook.destroy
    flash[:notice] = "Successfully deleted notebook."
    redirect_to notebooks_url
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_notebook
    @notebook = Notebook.find(params[:id])
  end
  
  def notebook_params
    params.fetch(:notebook, {}).permit(:title, :attachment_attributes => [:id, :data, :_destroy])   
  end
    
end

