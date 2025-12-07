import { useEffect, useState } from "react";
import './dashboard.css';

const Dashboard = () => {

  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/process")   // your API
      .then(res => res.json())
      .then(result => setData(result))
      .catch(err => console.error("Error:", err));
  }, []);

  return (
    <div className="dmain">
      <div className="dcont">
        <div className="dfstc">
          <div className="dcontainer">
            <div className="dfirst">
              <div id="one" className="dcol">
                {data ? data.one : "fst"}
              </div>
              <div id="two" className="dcol">
                {data ? data.two : "snd"}
              </div>
              <div id="three" className="dcol">
                {data ? data.three : "trd"}
              </div>
              <div id="four" className="dcol">
                {data ? data.four : "fth"}
              </div>
            </div>

            <div className="dsecond">
              <div id="five" className="dcol1">
                {data ? data.five : "fft"}
              </div>
              <div id="six" className="dcol1">
                {data ? data.six : "sth"}
              </div>
              <div id="seven" className="dcol1">
                {data ? data.seven : "svt"}
              </div>
              <div id="eight" className="dcol1">
                {data ? data.eight : "eth"}
              </div>
            </div>
          </div>
        </div>

        <div className="dsndc">
          <div id="sidechart" className="dsidechart">
            {data ? data.sidechart : "nth"}
          </div>
        </div>
      </div>

      <div className="dlower">
        <div id="chart1" className="dchart">
          {data ? data.chart1 : "tth"}
        </div>
        <div id="chart2" className="dchart">
          {data ? data.chart2 : "elv"}
        </div>
      </div>

      <div className="summary">
        {data ? data.summary : ""}
      </div>
    </div>
  );
};

export default Dashboard;
