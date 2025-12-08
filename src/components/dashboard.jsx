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
                <div>{data ? data.onename : "fst"}</div>
                <div>{data ? data.one : "fst"}</div>
              </div>
              <div id="two" className="dcol">
                <div>{data ? data.twoname : "fst"}</div>
                <div>{data ? data.two : "snd"}</div>
              </div>
              <div id="three" className="dcol">
                <div>{data ? data.threename : "fst"}</div>
                <div>{data ? data.three : "trd"}</div>
              </div>
              <div id="four" className="dcol">
                <div>{data ? data.fourname : "fst"}</div>
                <div>{data ? data.four : "fth"}</div>
              </div>
            </div>

            <div className="dsecond">
              <div id="five" className="dcol1">
                <div>{data ? data.fivename : "fst"}</div>
                <div>{data ? data.five : "fft"}</div>
              </div>
              <div id="six" className="dcol1">
                <div>{data ? data.sixname : "fst"}</div>
                <div>{data ? data.six : "sth"}</div>
              </div>
              <div id="seven" className="dcol1">
                <div>{data ? data.sevenname : "fst"}</div>
                <div>{data ? data.seven : "svt"}</div>
              </div>
              <div id="eight" className="dcol1">
                <div>{data ? data.eightname : "fst"}</div>
                <div>{data ? data.eight : "eth"}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="dsndc">
          <div id="sidechart" className="dsidechart">
            <div>{data ? data.sidechartname : "fst"}</div>
            {/* <div>{data ? data.sidechart : "nth"}</div> */}
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
          {data ? data.chart1name : "fst"}
          {/* {data ? data.chart1 : "tth"} */}
          {c1 && (
            <Plot
              data={c1.data}
              layout={c1.layout}
              style={{ width: "100%", height: "100%" }}
            />
            )}
        </div>
        <div id="chart2" className="dchart">
          {data ? data.chart2name : "fst"}
          {/* {data ? data.chart2 : "elv"} */}
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
