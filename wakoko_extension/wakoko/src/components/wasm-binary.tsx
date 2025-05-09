
import WASMListener, {BaseWASMListener} from "models/wasm.listener";
import * as React from "react";
import GraphData from "./graph.data";
import Graph from "./graph.view";
import CovPlot from "./plot";
import { Progress, Card, InputNumber, Form, Row, Col, Switch, Input, Alert } from 'antd';
import { DownloadOutlined, DownSquareFilled, BoxPlotOutlined } from '@ant-design/icons';
import TreeMap from "./tree.map";
import LocalStorageService from "services/local.storage.service";

export interface WasmBinaryProps {
	module: BaseWASMListener;
	page: string;
	index: number;
}

export interface WasmBinaryState {
	history: number[],
	pollingTime: number,
	nodes: {
		[key: number]: boolean
	}
	links: {
		target: number,
		source: number
	}[]
}

class WasmBinary extends React.Component<WasmBinaryProps, WasmBinaryState> {


	constructor(props: WasmBinaryProps){
	  super(props);
		
	  this.state = {
		  pollingTime: 1000,
		  history: [],
		  nodes: {},
		  links: []
	  }
	  this.download = this.download.bind(this)
	}
  
	time: any;

	componentDidMount(){
		this.time = setInterval(this.collectValues, this.state.pollingTime)
	}

	componentWillUnmount(){
		if(this.time)
			clearInterval(this.time)
	}

	collectValues = () => {

		this.props.module.getBlockCoverage(true)
		this.props.module.setVisitedMap(true)

		this.setState({
			history: [...this.props.module.history]
		})
	}

	onValChange = (val) => {
		if(this.time)
			clearInterval(this.time)
		
			this.setState({
				pollingTime: val
			}, () => {
				this.time = setInterval(this.collectValues, this.state.pollingTime)
			});
	}

   download(){
		  
	  var atag = document.createElement("a");
	  var file = new Blob([this.props.module.original],
		{type: "application/octet-stream"});
	  atag.href = URL.createObjectURL(file);
	  atag.download = `${this.props.page}${this.props.index}.wasm`;
	  atag.click();
	  atag.remove();
	}

	downloadCSV(){
		
		if(this.state.history){
			var atag = document.createElement("a");
			// @ts-ignore
			var file = new Blob([this.state.history.reduce((p, c) => `${p},${c}`)],
					{ type: "text/plain;charset=utf-8" });
			atag.href = URL.createObjectURL(file);
			atag.download = "cov.csv";
			atag.click();
		}

	}

	downloadInstrumented(){
		  
		var atag = document.createElement("a");
		var file = new Blob([new Uint8Array(this.props.module.instrumented)],
		  {type: "application/octet-stream"});
		atag.href = URL.createObjectURL(file);
		atag.download = `${this.props.page}${this.props.index}.instrumented.wasm`;
		atag.click();
		atag.remove();
	  }
	
	render(){
		const layout = {
		  };
		const lastVisited = this.state.history.slice(-1)[0] 
		const percent = Number((100*lastVisited/this.props.module.totalBlocks).toFixed(2));
	  return (<Card 
	  cover={
	  <React.Fragment>
		  <CovPlot values={this.state.history.map(t => 1.0*t/this.props.module.totalBlocks)} opened={true}/>
		  {/*<TreeMap functions={this.props.module.meta.map} hitMap={this.props.module.blockMap} blockCount={this.props.module.totalBlocks}/>*/}
	</React.Fragment>}
	  actions={[
		<BoxPlotOutlined key="setting" title="Download time data" onClick={() => this.downloadCSV()} />,
		<DownloadOutlined key="edit" title="Download original binary" onClick={() => this.download()}/>,
		<DownSquareFilled key="ellipsis" title="Download instrumented binary" onClick={() => this.downloadInstrumented()}/>,
	  ]}
	  ><div style={{padding: '2px'}}>
					<Progress showInfo percent={percent} />
					<Form
					{...layout}>
						<Row gutter={24}>
							<Col span={12}>
								<Form.Item
									label="Polling time"
								>
									<InputNumber onChange={this.onValChange} min={500} value={this.state.pollingTime} placeholder={"Polling interval time (ms)"}/>
								</Form.Item>
							</Col>
						</Row>
						

					</Form>
					{/*<GraphData links={this.state.links} nodes={this.state.nodes}/>*/}
		  </div></Card>)
	}
  }

  export default WasmBinary;