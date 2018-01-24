require 'test_helper'

class AnalysisTest < ActiveSupport::TestCase
  
  test "when created, should have a driver discipline" do
    mda = Analysis.create!( {name: 'NewMDA'} )
    assert mda.valid?
    assert_equal 1, mda.disciplines.count
    assert_equal WhatsOpt::Discipline::NULL_DRIVER_NAME, mda.disciplines.first.name
  end
   
  test "should create an mda from a mda template excel file" do
    attach = sample_file('excel_mda_simple_sample.xlsx')
    mda = Analysis.create!(attachment_attributes: {data: attach})
    assert mda.to_mda_viewer_json
    assert mda.valid?
    assert_equal 3, mda.design_variables.count
    assert_equal 1, mda.optimization_variables.count
  end

  test "should be able to build nodes" do
    mda = analyses(:cicav)
    assert_equal %w[Geometry Aerodynamics], mda.build_nodes.map {|n| n[:name]} 
  end
  
  test "should be able to build connections from user" do
    mda = analyses(:cicav)
    geo = disciplines(:geometry).id.to_s
    aero = disciplines(:aerodynamics).id.to_s
    u = "_U_"
    edges = mda.build_edges
    assert_equal 7, edges.count
    assert_includes edges, {from: geo, to: aero, name: "y,z"}
    assert_includes edges, {from: aero, to: geo, name: "x"}
    assert_includes edges, {from: u, to: geo, name: "z"}
    assert_includes edges, {from: u, to: geo, name: "z"}
    assert_includes edges, {from: u, to: aero, name: "z"}
    assert_includes edges, {from: aero, to: u, name: "z_pending"}
    assert_includes edges, {from: u, to: geo, name: "x_pending"}
  end
  
  test "should not contain reflexive connection" do
    mda = analyses(:cicav)
    edges = mda.build_edges
    assert_empty edges.select {|e| e[:to] == e[:from] }
  end
  
  test "should be able to build variable list" do
    mda = analyses(:cicav)
    tree = mda.build_var_infos
    assert_equal mda.disciplines.nodes.all.map(&:id), tree.keys
    geom_id = Discipline.where(name: 'Geometry').first.id
    aero_id = Discipline.where(name: 'Aerodynamics').first.id
    assert_equal ["x_pending", "x", "z"], tree[geom_id][:in].map{|h| h[:name]}
    assert_equal ["y", "z"], tree[geom_id][:out].map{|h| h[:name]}
    assert_equal ["z", "y"], tree[aero_id][:in].map{|h| h[:name]}
    assert_equal ["x", "z_pending"], tree[aero_id][:out].map{|h| h[:name]}
  end
 
end
