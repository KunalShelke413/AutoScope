import { useEffect, useState } from "react";
import './dashboard.css';
import Plot from "react-plotly.js";

const Dashboard = () => {

  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/process")   // your API
      .then(res => res.json())
      .then(result => setData(result))
      .catch(err => console.error("Error:", err));
  }, []);

  const [pc1, Plt1] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/p1plot")   // your API
      .then(res => res.json())
      .then(data => Plt1(data))
      .catch(err => console.error(err));
  }, []);

  const [pc2, Plt2] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/p2plot")   // your API
      .then(res => res.json())
      .then(data => Plt2(data))
      .catch(err => console.error(err));
  }, []);

  const [pc3, Plt3] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/p3plot")   // your API
      .then(res => res.json())
      .then(data => Plt3(data))
      .catch(err => console.error(err));
  }, []);

const [pc4, Plt4] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/p4plot")   // your API
      .then(res => res.json())
      .then(data => Plt4(data))
      .catch(err => console.error(err));
  }, []);

  const [sidec, PlotData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/sideplot")   // your API
      .then(res => res.json())
      .then(data => PlotData(data))
      .catch(err => console.error(err));
  }, []);

  const [c1, PlotData1] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/chart1plot")   // your API
      .then(res => res.json())
      .then(data => PlotData1(data))
      .catch(err => console.error(err));
  }, []);

  const [c2, PlotData2] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/chart2plot")   // your API
      .then(res => res.json())
      .then(data => PlotData2(data))
      .catch(err => console.error(err));
  }, []);
  return (
    <div className="dmain">
      <div className="dcont">
        <div className="dfstc">
          <div className="dcontainer">
            <div className="dfirst">
              <div id="one" className="dcol">
                <div style={{ color: "black" }}>{data ? data.onename : "fst"}</div>
                <div style={{ color: "black" }}>{data ? data.one : "fst"}</div>
              </div>
              <div id="two" className="dcol">
                <div style={{ color: "black" }}>{data ? data.twoname : "fst"}</div>
                <div style={{ color: "black" }}>{data ? data.two : "snd"}</div>
              </div>
              <div id="three" className="dcol">
                <div style={{ color: "black" }}>{data ? data.threename : "fst"}</div>
                <div style={{ color: "black" }}>{data ? data.three : "trd"}</div>
              </div>
              <div id="four" className="dcol">
                <div style={{ color: "black" }}>{data ? data.fourname : "fst"}</div>
                <div style={{ color: "black" }}>{data ? data.four : "fth"}</div>
              </div>
            </div>

            <div className="dsecond">
              <div id="five" className="dcol1">
                {/*<div>{data ? data.fivename : "fst"}</div>
                <div>{data ? data.five : "fft"}</div>*/}
                {pc1 && (
                  <Plot
                    data={pc1.data}
                    layout={pc1.layout}
                    style={{ width: "100%", height: "100%" }}
                  />
                )}
              </div>
              <div id="six" className="dcol1">
                {/*<div>{data ? data.sixname : "fst"}</div>
                <div>{data ? data.six : "sth"}</div>*/}
                {pc2 && (
                  <Plot
                    data={pc2.data}
                    layout={pc2.layout}
                    style={{ width: "100%", height: "100%" }}
                  />
                )}
              </div>
              <div id="seven" className="dcol1">
                {/*<div>{data ? data.sevenname : "fst"}</div>
                <div>{data ? data.seven : "svt"}</div>*/}
                {pc3 && (
                  <Plot
                    data={pc3.data}
                    layout={pc3.layout}
                    style={{ width: "100%", height: "100%" }}
                  />
                )}
              </div>
              <div id="eight" className="dcol1">
                {/*<div>{data ? data.eightname : "fst"}</div>
                <div>{data ? data.eight : "eth"}</div>*/}
                {pc4 && (
                  <Plot
                    data={pc4.data}
                    layout={pc4.layout}
                    style={{ width: "100%", height: "100%" }}
                  />
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="dsndc">
          <div id="sidechart" className="dsidechart">
            {/* <div>{data ? data.sidechartname : "fst"}</div>
            <div>{data ? data.sidechart : "nth"}</div> */}
            {sidec && (
            <Plot
              data={sidec.data}
              layout={sidec.layout}
              style={{ width: "100%", height: "100%" }}
            />
            )}
          </div>
        </div>
      </div>

      <div className="dlower">
        <div id="chart1" className="dchart">
          {/* {data ? data.chart1name : "fst"}
          {data ? data.chart1 : "tth"} */}
          {c1 && (
            <Plot
              data={c1.data}
              layout={c1.layout}
              style={{ width: "100%", height: "100%" }}
            />
            )}
        </div>
        <div id="chart2" className="dchart">
          {/* {data ? data.chart2name : "fst"}
          {data ? data.chart2 : "elv"} */}
          {c2 && (
            <Plot
              data={c2.data}
              layout={c2.layout}
              style={{ width: "100%", height: "100%" }}
            />
            )}
        </div>
      </div>

      <div className="summary">
        {data ? data.summary : "change me"}
      </div>
    </div>
  );
};

export default Dashboard;
