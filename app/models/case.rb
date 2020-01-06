# frozen_string_literal: true

class Case < ApplicationRecord
  serialize :values

  belongs_to :operation
  belongs_to :variable

  scope :with_role_case, ->(role) { includes(:variable).references(:variables).joins("variables.outgoing_connections").where(connections: { role: role }).uniq }
  scope :inputs, ->(ope) { Case.where(operation: ope).with_role_case(WhatsOpt::Variable::INTEREST_INPUT_ROLES) }
  scope :outputs, ->(ope) { Case.where(operation: ope).with_role_case(WhatsOpt::Variable::INTEREST_OUTPUT_ROLES) }

  def nb_of_points
    values.size
  end

  def float_varname
    label
  end

  def label
    @label ||= Case.labelOf(variable.name, coord_index) 
  end

  def self.labelOf(name, coord)
    name + (coord < 0 ? "" : "[#{coord}]")
  end

  def build_copy(operation, variable)
    copy = self.dup
    copy.variable = variable
    copy.operation = operation
    copy
  end
end
