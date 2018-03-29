class CreateCases < ActiveRecord::Migration[5.1]
  def change
    create_table :cases do |t|
      t.integer :operation_id
      t.integer :variable_id
      t.text :values
    end
  end
end
