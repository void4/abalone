<template>
  <div style="width:50%;">
    <canvas id="myChart" width="400" height="400"></canvas>
  </div>
  <!--<img alt="Vue logo" src="../assets/graph.png">-->
</template>

<script>
import axios from 'axios';
import * as chart from '../assets/Chart.min.js';

function range(start, stop, step) {
    var a = [start.toString()], b = start;
    while (b < stop) {
        a.push((b += step || 1).toString());
    }
    return a;
}

export default {
  name: 'Stats',
  data() {
    return {
    };
  },
  components: {
  },
  methods: {
    getRatings() {
      const path = `${window.location.protocol}//${window.location.hostname}:5000/ratings`;
      axios.get(path)
        .then((res) => {
          //console.log(res)
          var labels = range(1, res.data[0].data.length)
          //console.log(labels)
          var ctx = document.getElementById('myChart').getContext('2d');
          var config =  {
              type: 'line',
              data: {
                labels: labels,
                datasets: res.data
              },
              options: {
                responsive: true,
                title: {
                  display: true,
                  text: 'Player Ratings'
                },
                tooltips: {
                  mode: 'index',
                  intersect: false,
                },
        				scales: {
        					xAxes: [{
                    type: 'linear',
        						display: true,
        						scaleLabel: {
        							display: true,
        							labelString: 'Time'
        						}
        					}],
        					yAxes: [{
                    type: 'linear',
        						display: true,
        						scaleLabel: {
        							display: true,
        							labelString: 'Rating'
        						}
        					}]
        				}
              }
          }
          console.log(config)
          this.myChart = new Chart(ctx, config);
          //this.myChart.update();

        })
        .catch((error) => {
          // eslint-disable-next-line
                    console.error(error);
        });
    },
  },
  mounted() {
    this.getRatings();
  },
};
</script>
