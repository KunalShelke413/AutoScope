import { useEffect, useState } from "react";
import './dashboard.css';
import Plot from "react-plotly.js";

const Dashboard = () => {
  /* -------------------- STATES -------------------- */
  const [data, setData] = useState(null);

  const [pc1, setPc1] = useState(null);
  const [pc2, setPc2] = useState(null);
  const [pc3, setPc3] = useState(null);
  const [pc4, setPc4] = useState(null);

  const [sidec, setSidec] = useState(null);
  const [c1, setC1] = useState(null);
  const [c2, setC2] = useState(null);

  const [des, setDes] = useState(null);   // categorical summary
  const [ndes, setNdes] = useState(null); // numerical summary

  /* -------------------- FETCHES -------------------- */
  useEffect(() => {
    fetch("http://localhost:8000/process")
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/p1plot").then(r => r.json()).then(setPc1);
    fetch("http://localhost:8000/p2plot").then(r => r.json()).then(setPc2);
    fetch("http://localhost:8000/p3plot").then(r => r.json()).then(setPc3);
    fetch("http://localhost:8000/p4plot").then(r => r.json()).then(setPc4);
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/sideplot").then(r => r.json()).then(setSidec);
    fetch("http://localhost:8000/chart1plot").then(r => r.json()).then(setC1);
    fetch("http://localhost:8000/chart2plot").then(r => r.json()).then(setC2);
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/alpdes").then(r => r.json()).then(setDes);
    fetch("http://localhost:8000/numdes").then(r => r.json()).then(setNdes);
  }, []);

  /* -------------------- LOADING -------------------- */
  if (!des || !ndes) {
    return <p style={{ padding: "20px" }}>Loading dashboard...</p>;
  }

  /* -------------------- DYNAMIC TABLE DATA -------------------- */
  const catColumns = Object.keys(des);
  const catRows = Object.keys(des[catColumns[0]]);

  const numColumns = Object.keys(ndes);
  const numRows = Object.keys(ndes[numColumns[0]]);


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
      <div className="info">
        <div className="alpha">
          <div className="title_name">Categorical Columns</div>
          <div >
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead style={{ position: "sticky", top: 0, background: "red" }}>
                <tr>
                  <th style={thStyle}>Metric</th>
                  {catColumns.map(col => (
                    <th key={col} style={thStyle}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {catRows.map(row => (
                  <tr key={row}>
                    <td style={tdStyle}><b>{row}</b></td>
                    {catColumns.map(col => (
                      <td key={col} style={tdStyle}>{des[col][row] ?? "-"}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className="numb">
          <div className="title_name">Numerical Columns</div>
          <div>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead style={{ position: "sticky", top: 0, background: "red" }}>
                <tr>
                  <th style={thStyle}>Metric</th>
                  {numColumns.map(col => (
                    <th key={col} style={thStyle}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {numRows.map(row => (
                  <tr key={row}>
                    <td style={tdStyle}><b>{row}</b></td>
                    {numColumns.map(col => (
                      <td key={col} style={tdStyle}>{ndes[col][row] ?? "-"}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div className="summary_graph">
        <div className="df_colname">column name</div>
        <div className="col_and_grp">
          <div className="df_summary">about graph</div>
          <div className="df_grp_box">
            <div className="grp_type">line,bar,pie</div>
            <div className="df_grp">grp</div>
          </div>
        </div>
      </div>

      {/* <div className="summary">
        {data ? data.summary : "change me"}
      </div> */}
    </div>
  );
};

const thStyle = {
  border: "1px solid gray",
  padding: "5px",
  fontWeight: "bold"
};

const tdStyle = {
  border: "1px solid gray",
  padding: "6px",
  fontSize: "13px"
  
};

export default Dashboard;
