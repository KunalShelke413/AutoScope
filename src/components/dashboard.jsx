import { useEffect, useState } from "react";
import './dashboard.css';
import Plot from "react-plotly.js";

const Dashboard = () => {
  /* -------------------- STATES -------------------- */
  const [data, setData] = useState(null);

  const [pc1, setPc1] = useState(null); //k_pie1
  const [pc2, setPc2] = useState(null); //k_pie2
  const [pc3, setPc3] = useState(null); //k_pie3
  const [pc4, setPc4] = useState(null); //k_pie4

  const [sidec, setSidec] = useState(null); //heatmap
  const [c1, setC1] = useState(null); //chart1
  const [c2, setC2] = useState(null); //chart2

  const [des, setDes] = useState(null);   // categorical summary
  const [ndes, setNdes] = useState(null); // numerical summary

  const [cols, setCols] = useState([]);

  const [activeCol, setActiveCol] = useState(null);
  const [activeChartType, setActiveChartType] = useState(null);

  const [Rcharts, setRCharts] = useState({}); //bar
  const [PRcharts, setPRCharts] = useState({}); //pie
  const [LRcharts, setLRCharts] = useState({}); //line
  const [HGRcharts, setHGRCharts] = useState({}); //histogram
  const [SRcharts, setSRCharts] = useState({}); //scatter
  const [BRcharts, setBRCharts] = useState({}); //box
  const [ARcharts, setARCharts] = useState({}); //area
  const [BLRcharts, setBLRCharts] = useState({}); //bubble


  const [currentIndex, setCurrentIndex] = useState(0); //grp setting
  const [currentFigures, setCurrentFigures] = useState([]); //grp setting



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

  useEffect(() => {
    fetch("http://localhost:8000/allcol")
      .then(r => r.json())
      .then(data => setCols(data.columns))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/process_filtered_result")
      .then(res => res.json())
      .then(data => setRCharts(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/process_filtered_pie_result")
      .then(res => res.json())
      .then(data => setPRCharts(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/process_filtered_line_result")
      .then(res => res.json())
      .then(data => setLRCharts(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/process_filtered_histogram_result")
      .then(res => res.json())
      .then(data => setHGRCharts(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/process_filtered_scatter_result")
      .then(res => res.json())
      .then(data => setSRCharts(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/process_filtered_box_result")
      .then(res => res.json())
      .then(data => setBRCharts(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/process_filtered_area_result")
      .then(res => res.json())
      .then(data => setARCharts(data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/process_filtered_bubble_result")
      .then(res => res.json())
      .then(data => setBLRCharts(data))
      .catch(err => console.error(err));
  }, []);
  /*------------------------grp_setting------------------------*/

  useEffect(() => {
    setCurrentIndex(0);
  }, [activeCol, activeChartType]);


  useEffect(() => {
    if (!activeCol || !activeChartType) {
      setCurrentFigures([]);
      return;
    }

    let selectedCharts = null;

    if (activeChartType === "Bar chart") {
      selectedCharts = Rcharts;
    } else if (activeChartType === "Line chart") {
      selectedCharts = LRcharts;
    } else if (activeChartType === "Pie chart") {
      selectedCharts = PRcharts;
    }else if (activeChartType === "Histogram chart") {
      selectedCharts = HGRcharts;
    } else if (activeChartType === "Scatter plot") {
      selectedCharts = SRcharts;
    } else if (activeChartType === "Box plot") {
      selectedCharts = BRcharts;
    } else if (activeChartType === "Area chart") {
      selectedCharts = ARcharts;
    } else if (activeChartType === "Bubble chart") {
      selectedCharts = BLRcharts;
    } else {
      setCurrentFigures([]);
      return;
    }

    const figs = selectedCharts?.[activeCol] || [];
    setCurrentFigures(figs);

  }, [activeCol, activeChartType, Rcharts, PRcharts, LRcharts, HGRcharts, SRcharts, BRcharts, ARcharts, BLRcharts]);


  /*------------------------grp_setting------------------------*/

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
      <div className="summary_title"><p>Describe columns and Grap based on columns:</p></div>
      <div className="summary_graph">
        <div className="df_colname">
          {cols.map((col, index) => (
            <button key={index} className={`col-btn ${activeCol === col ? "active" : ""}`}
              onClick={() => {
                setActiveCol(col);
              }}
            >
              {col}
            </button>
          ))}
        </div>
        <div className="col_and_grp">
          <div className="df_summary">about graph</div>
          <div className="df_grp_box">
            <div className="grp_type">
              <ul>
                {[
                  "Bar chart",
                  "Line chart",
                  "Pie chart",
                  "Histogram chart",
                  "Scatter plot",
                  "Box plot",
                  "Area chart",
                  "Bubble chart"
                ].map((type) => (
                  <li
                    key={type}
                    className={activeChartType === type ? "active" : ""}
                    onClick={() => setActiveChartType(type)}
                  >
                    {type}
                  </li>
                ))}
              </ul>
            </div>

            <div className="df_grp">
              {currentFigures.length > 0 ? (
                <>
                  {currentFigures[currentIndex] && (
                    <Plot
                      data={currentFigures[currentIndex].data}
                      layout={currentFigures[currentIndex].layout}
                      style={{ width: "100%", height: "400px" }}
                    />
                  )}

                  {currentFigures.length > 1 && (
                    <div className="nav_buttons">
                      <button
                        onClick={() =>
                          setCurrentIndex(i => Math.max(i - 1, 0))
                        }
                        disabled={currentIndex === 0}
                      >
                        ◀
                      </button>

                      <span style={{ margin: "0 10px" }}>
                        {currentIndex + 1} / {currentFigures.length}
                      </span>

                      <button
                        onClick={() =>
                          setCurrentIndex(i =>
                            Math.min(i + 1, currentFigures.length - 1)
                          )
                        }
                        disabled={currentIndex === currentFigures.length - 1}
                      >
                        ▶
                      </button>
                    </div>
                  )}
                </>
              ) : (
                <p style={{ padding: "10px" }}>
                  Select a column and chart type
                </p>
              )}
            </div>


          </div>
        </div>
      </div>


      <div className="summary">
        {data ? data.summary : "summary"}
      </div>
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
