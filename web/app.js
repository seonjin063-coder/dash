document.addEventListener('DOMContentLoaded', () => {
    // 1. Python이 만들어둔 JSON 데이터 로드
    fetch('../output/dashboard_data.json')
        .then(response => {
            if (!response.ok) throw new Error('Data load failed');
            return response.json();
        })
        .then(data => {
            renderFocusGauge(data.focus_gauge);
            renderNetworkMap(data.network);
            renderTimeline(data.timeline);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('focusList').innerHTML = 
                `<div style="color:#ff6b6b; padding: 1rem;">
                    [시스템 오류] 네트워크 데이터를 불러오지 못했습니다.<br><br>
                    1. 파이썬 스크립트 실행이 완료되었는지 확인하세요.<br>
                    2. 이 HTML 파일을 단순히 더블클릭해서 열었다면 브라우저 보안 정책(CORS)에 막힌 것입니다. 로컬 웹 서버(python -m http.server 8000)를 통해 접속해 주세요.
                </div>`;
        });
});

// 1. Focus Gauge (리스트 렌더링)
function renderFocusGauge(focusData) {
    const listContainer = document.getElementById('focusList');
    listContainer.innerHTML = '';

    focusData.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'list-item';
        div.innerHTML = `
            <div class="item-header">
                <div class="item-rank">0${index + 1}</div>
                <div class="item-score">피인용 ${item.citations}회</div>
            </div>
            <div class="item-title">${item.title}</div>
            <div class="item-meta">
                ${item.author} | ${item.journal} | ${item.year ? item.year + '년' : '-'}
            </div>
        `;
        listContainer.appendChild(div);
    });
}

// 2. Navigation (네트워크 맵)
function renderNetworkMap(networkData) {
    const chartDom = document.getElementById('networkChart');
    const myChart = echarts.init(chartDom);
    
    // 차트 성능과 직관성을 위해 선(Edge)은 상위 100개만 필터링
    const links = networkData.links.sort((a,b) => b.value - a.value).slice(0, 100);

    const option = {
        tooltip: { formatter: '{b}' },
        series: [{
            type: 'graph',
            layout: 'force',
            force: {
                repulsion: 250,
                edgeLength: [50, 100],
                gravity: 0.1
            },
            data: networkData.nodes.map(node => {
                const isHighlight = ['자유', '사르트르', '실존주의'].includes(node.name);
                const size = Math.max(15, Math.min(45, node.value * 2.5));
                return {
                    name: node.name,
                    value: node.value,
                    symbolSize: isHighlight ? size * 1.5 : size, // 중요 노드 크기 확대
                    itemStyle: {
                        color: isHighlight ? '#00d2ff' : '#2a4b8d',
                        borderColor: isHighlight ? '#fff' : 'transparent',
                        borderWidth: isHighlight ? 2 : 0,
                        shadowBlur: isHighlight ? 20 : 0,
                        shadowColor: '#00d2ff'
                    },
                    label: {
                        show: size > 25 || isHighlight,
                        color: isHighlight ? '#fff' : '#cbd5e1',
                        fontSize: isHighlight ? 14 : 11,
                        fontWeight: isHighlight ? 'bold' : 'normal'
                    }
                }
            }),
            links: links,
            roam: true,
            label: { position: 'right' },
            lineStyle: {
                color: 'source',
                curveness: 0.3,
                opacity: 0.4
            },
            emphasis: {
                focus: 'adjacency',
                lineStyle: { width: 4, opacity: 0.8 }
            }
        }]
    };
    
    myChart.setOption(option);
    window.addEventListener('resize', () => myChart.resize());
}

// 3. Timeline (영역 꺾은선)
function renderTimeline(timelineData) {
    const chartDom = document.getElementById('timelineChart');
    const myChart = echarts.init(chartDom);

    timelineData.sort((a,b) => a.year - b.year); // 연도 오름차순
    
    const years = timelineData.map(d => d.year.toString());
    const counts = timelineData.map(d => d.count);

    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'line' },
            backgroundColor: 'rgba(15, 17, 21, 0.9)',
            borderColor: '#333',
            textStyle: { color: '#fff' }
        },
        grid: {
            top: '15%', left: '3%', right: '4%', bottom: '5%', containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: years,
            axisLabel: { color: '#94a3b8' },
            axisLine: { lineStyle: { color: '#333' } }
        },
        yAxis: {
            type: 'value',
            minInterval: 1,
            axisLabel: { color: '#94a3b8' },
            splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)', type: 'dashed' } }
        },
        series: [
            {
                name: '논문 발행 건수',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 8,
                itemStyle: { color: '#00d2ff' },
                lineStyle: {
                    width: 3,
                    shadowColor: 'rgba(0, 210, 255, 0.4)',
                    shadowBlur: 10
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(0, 210, 255, 0.4)' },
                        { offset: 1, color: 'rgba(0, 210, 255, 0.0)' }
                    ])
                },
                data: counts
            }
        ]
    };

    myChart.setOption(option);
    window.addEventListener('resize', () => myChart.resize());
}
