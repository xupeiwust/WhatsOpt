import React from 'react';
import Plot from 'react-plotly.js';
import update from 'immutability-helper'
import { analysisDatabase } from '../../utils/AnalysisDatabase';

class ScatterPlotMatrix extends React.Component {
    
  constructor(props) {
    super(props);
    this.db = analysisDatabase(this.props.mda)
  }
  
  render() {
    let cases = this.props.ope.cases;
    cases.sort(this._sortCases);
    
    let designVarCases = cases.filter(c => { return this.db.isDesignVarCases(c); })
    let outputVarCases = cases.filter(c => { return this.db.isOutputVarCases(c) })
    let couplingVarCases = cases.filter(c => { return this.db.isCouplingVarCases(c) })
    
    let inputs = designVarCases.concat(couplingVarCases);
    let outputs = couplingVarCases.concat(outputVarCases);
    
    let data = [];
    let layout = {};
    let nOut = outputs.length;
    let nDes = inputs.length;
    let pdh = 1./nDes;
    let pdv = 1./nOut;

    for (let i=0; i<nOut; i++) {
      for (let j=0; j<nDes; j++) {
        let xlabel = inputs[j].varname;
        xlabel += inputs[j].coord_index===-1?"":" "+inputs[j].coord_index;
        let ylabel = outputs[i].varname;
        ylabel += outputs[i].coord_index===-1?"":" "+outputs[i].coord_index;
    
        let trace = { x: inputs[j].values, y: outputs[i].values, 
                      type: 'scatter', mode: 'markers'};
        let n = nDes*i+j+1;
        let xname = 'x'+n;
        let yname = 'y'+n;
        trace.xaxis = xname;
        trace.yaxis = yname;
        trace.name = ylabel + " vs " + xlabel;
        data.push(trace);

        layout['xaxis'+n] = {domain: [(j+0.1)*pdh, (j+0.9)*pdh], anchor: yname};
        layout['yaxis'+n] = {domain: [(i+0.1)*pdv, (i+0.9)*pdv], anchor: xname};
        if (j===0) {
          layout['yaxis'+n].title = ylabel;
        }  
        if (i===0) {
          layout['xaxis'+n].title = xlabel;
        }
      } 
    }
    layout.width = nDes*250;
    layout.height = nOut*250;
    
    let title = "Scatterplot Matrix";
    layout.title  = title;

    return (<Plot data={data} layout={layout} />);
  }
  
  _sortCases(a, b) {
    if (a.varname === b.varname) {
      return a.coord_index < b.coord_index ? -1:1
    } 
    return a.varname.localeCompare(b.varname);
  }
}

export default ScatterPlotMatrix;