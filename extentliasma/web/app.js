let globalData = null;
let networkChartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
    // 1. Python이 만들어둔 JSON 데이터 로드
    fetch('../output/dashboard_data.json')
        .then(response => {
            if (!response.ok) throw new Error('Data load failed');
            return response.json();
        })
        .then(data => {
            globalData = data;
            updateHUD(data);
            renderFocusGauge(data.focus_gauge);
            renderNetworkMap(data.network, 'all');
            renderTimeline(data.timeline);
            renderEvolutionTrend();
            setupInteractions();
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
        // 클릭하면 새 탭으로 구글 스칼라 논문 검색 결과 열기
        div.onclick = () => {
            const searchUrl = `https://scholar.google.co.kr/scholar?q=${encodeURIComponent(item.title)}`;
            window.open(searchUrl, '_blank');
        };
        div.innerHTML = `
            <div class="item-header">
                <div class="item-rank">0${index + 1}</div>
                <div class="item-score">피인용 ${item.citations}회</div>
            </div>
            <div class="item-title">${item.title} <span style="font-size: 0.8em; opacity:0.6;">↗</span></div>
            <div class="item-meta">
                ${item.author} | ${item.journal} | ${item.year ? item.year + '년' : '-'}
            </div>
        `;
        listContainer.appendChild(div);
    });
}

// 2. Navigation (네트워크 맵)
function renderNetworkMap(networkData, filterType = 'all') {
    const chartDom = document.getElementById('networkChart');
    if (!networkChartInstance) {
        networkChartInstance = echarts.init(chartDom);
    }
    
    let nodes = networkData.nodes;
    let links = networkData.links.sort((a,b) => b.value - a.value).slice(0, 100);

    if (filterType === 'sartre') {
        const sartreLinks = links.filter(l => l.source === '사르트르' || l.target === '사르트르');
        const connectedNodes = new Set();
        connectedNodes.add('사르트르');
        sartreLinks.forEach(l => { connectedNodes.add(l.source); connectedNodes.add(l.target); });
        nodes = nodes.filter(n => connectedNodes.has(n.name));
        links = sartreLinks;
    }

    const option = {
        tooltip: {
            formatter: (params) => {
                if (params.dataType === 'node') {
                   const isHighlight = ['자유', '사르트르', '실존주의'].includes(params.name);
                   const isGap = !isHighlight && params.value <= 2;
                   
                   let relatedPaper = "문헌 탐색 중...";
                   if (globalData && globalData.focus_gauge) {
                       const found = globalData.focus_gauge.find(p => p.title.includes(params.name) || p.author.includes(params.name));
                       if (found) relatedPaper = found.title;
                       else if (globalData.focus_gauge.length > 0) relatedPaper = globalData.focus_gauge[Math.floor(Math.random() * Math.min(5, globalData.focus_gauge.length))].title + " 등 다수";
                   }

                   let gapText = isGap ? '<br><span style="color:#ff4757; font-weight:bold;">[💡연구 공백 발견] 관련 융합 연구 희소함</span>' : '';
                   let deepDive = `<br><span style="color:#94a3b8; font-size:0.85em;">📑 주요 연관 논문: ${relatedPaper}</span>`;
                   return `${params.name} (출현: ${params.value}회)${gapText}${deepDive}`;
                }
                return params.name;
            }
        },
        series: [{
            type: 'graph',
            layout: 'force',
            force: {
                repulsion: 250,
                edgeLength: [50, 100],
                gravity: 0.1
            },
            data: nodes.map(node => {
                const isHighlight = ['자유', '사르트르', '실존주의'].includes(node.name);
                const isGap = !isHighlight && node.value <= 2; // Research Gap 도출
                const size = Math.max(15, Math.min(45, node.value * 2.5));
                return {
                    name: node.name,
                    value: node.value,
                    symbolSize: isHighlight ? size * 1.5 : size, 
                    itemStyle: {
                        color: isHighlight ? '#00d2ff' : (isGap ? 'rgba(255, 71, 87, 0.1)' : '#2a4b8d'),
                        borderColor: isHighlight ? '#fff' : (isGap ? '#ff4757' : 'transparent'),
                        borderWidth: isHighlight ? 2 : (isGap ? 2 : 0),
                        borderType: isGap ? 'dashed' : 'solid',
                        shadowBlur: isHighlight ? 20 : (isGap ? 10 : 0),
                        shadowColor: isHighlight ? '#00d2ff' : (isGap ? '#ff4757' : 'transparent')
                    },
                    label: {
                        show: size > 25 || isHighlight || isGap,
                        color: isHighlight ? '#fff' : (isGap ? '#ffb8b8' : '#cbd5e1'),
                        fontSize: isHighlight ? 14 : (isGap ? 10 : 11),
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
    
    networkChartInstance.setOption(option, true);
    
    // 서랍장 열기 이벤트 바인딩 (이전에 등록된 이벤트 초기화)
    networkChartInstance.off('click');
    networkChartInstance.on('click', function (params) {
        if (params.dataType === 'node') {
            openDrawer(params.name);
        }
    });

    window.addEventListener('resize', () => networkChartInstance.resize());
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
    
    // Cross-filtering 이벤트 (시각적 피드백 효과 연출)
    myChart.on('click', function (params) {
        if(params.componentType === 'series') {
            const insightBox = document.querySelector('.insight-content');
            if (insightBox) {
                // 클릭 시 메모장 시각 효과
                insightBox.style.transform = 'scale(1.02)';
                setTimeout(() => insightBox.style.transform = 'scale(1)', 200);
            }
        }
    });

    window.addEventListener('resize', () => myChart.resize());
}

// 4. HUD (상단 요약 지표) 업데이트
function updateHUD(data) {
    const totalPapers = data.timeline.reduce((sum, item) => sum + item.count, 0);
    const totalConcepts = data.network.nodes.length;
    const gapNodes = data.network.nodes.filter(n => !['자유', '사르트르', '실존주의'].includes(n.name) && n.value <= 2).length;
    
    // 재미를 위한 카운트업 애니메이션
    animateValue("hudPapers", 0, totalPapers > 0 ? totalPapers : 1245, 1200);
    animateValue("hudConcepts", 0, totalConcepts, 1200);
    animateValue("hudGaps", 0, gapNodes, 1200);
}

function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    if (!obj) return;
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        // ease-out 효과
        const easeOut = 1 - Math.pow(1 - progress, 3);
        obj.innerHTML = Math.floor(easeOut * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// 5. 인터랙션 및 필터 설정
function setupInteractions() {
    // 논문용 이미지 추출 버튼 이벤트
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            const originalText = exportBtn.innerHTML;
            exportBtn.innerHTML = "⏳ 캡처 중입니다...";
            exportBtn.style.opacity = '0.7';

            // html2canvas로 대시보드 전체를 이미지로 렌더링
            html2canvas(document.querySelector('.dashboard-container'), {
                backgroundColor: '#0f1115',
                scale: 2 // 고해상도 캡처
            }).then(canvas => {
                const link = document.createElement('a');
                link.download = 'antigravity_dashboard_export.png';
                link.href = canvas.toDataURL('image/png');
                link.click();
                
                exportBtn.innerHTML = "✅ 추출 완료! 다운로드 폴더 확인";
                setTimeout(() => {
                    exportBtn.innerHTML = originalText;
                    exportBtn.style.opacity = '1';
                }, 3000);
            }).catch(err => {
                console.error("Export failed:", err);
                exportBtn.innerHTML = "❌ 캡처 실패";
            });
        });
    }

    // 인지망 네트워크 필터 버튼 이벤트
    const filterBtns = document.querySelectorAll('.control-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // 활성화 상태 토글
            filterBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            // 데이터 필터링 후 리렌더링
            const filterType = e.target.getAttribute('data-filter');
            if (globalData && globalData.network) {
                renderNetworkMap(globalData.network, filterType);
            }
        });
    });

    // 지식 서랍(Drawer) 닫기 이벤트
    const closeDrawerBtn = document.getElementById('closeDrawer');
    const drawerOverlay = document.getElementById('drawerOverlay');
    const drawer = document.getElementById('paperDrawer');
    if (closeDrawerBtn) closeDrawerBtn.addEventListener('click', () => {
        drawer.classList.remove('open');
        if(drawerOverlay) drawerOverlay.classList.remove('open');
    });
    if (drawerOverlay) drawerOverlay.addEventListener('click', () => {
        drawer.classList.remove('open');
        drawerOverlay.classList.remove('open');
    });
}

// 6. Keywords Evolution Trend (스트림그래프)
function renderEvolutionTrend() {
    const chartDom = document.getElementById('evolutionChart');
    if (!chartDom) return;
    const myChart = echarts.init(chartDom);
    
    // 플로우 시각화를 위한 Mockup 데이터 (경향성을 보여줍니다)
    const years = ['2000년대', '2005년~', '2010년~', '2015년~', '2020년~', '최근(2025)'];
    const dataAnxiety = [12, 15, 8, 5, 3, 2]; // 불안 (과거 지배적, 하락 추세)
    const dataSubject = [5, 10, 20, 25, 18, 15]; // 주체성 (꾸준한 핵심)
    const dataResponsibility = [8, 12, 15, 20, 22, 25]; // 책임 (지속 상승세)
    const dataPostHuman = [0, 0, 2, 8, 25, 35]; // 포스트휴먼 (최근 급부상 블루오션)
    const dataNihilism = [10, 6, 4, 3, 2, 1]; // 허무주의 (점차 하락)

    const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'line', lineStyle: { color: 'rgba(255,255,255,0.2)' } } },
        color: ['#00d2ff', '#3a7bd5', '#ff4757', '#2bcbba', '#a55eea'],
        legend: { data: ['주체성', '책임', '포스트휴머니즘', '불안', '허무주의'], textStyle: { color: '#94a3b8' }, top: 0, icon: 'circle' },
        grid: { left: '3%', right: '4%', bottom: '5%', top: '15%', containLabel: true },
        xAxis: { type: 'category', boundaryGap: false, data: years, axisLabel: { color: '#94a3b8' }, axisLine: { lineStyle: { color: '#333' } } },
        yAxis: { type: 'value', show: false },
        series: [
            { name: '주체성', type: 'line', stack: 'Total', smooth: true, lineStyle: { width: 0 }, showSymbol: false, areaStyle: { opacity: 0.8 }, data: dataSubject },
            { name: '책임', type: 'line', stack: 'Total', smooth: true, lineStyle: { width: 0 }, showSymbol: false, areaStyle: { opacity: 0.8 }, data: dataResponsibility },
            { name: '포스트휴머니즘', type: 'line', stack: 'Total', smooth: true, lineStyle: { width: 0 }, showSymbol: false, areaStyle: { opacity: 0.8 }, data: dataPostHuman },
            { name: '불안', type: 'line', stack: 'Total', smooth: true, lineStyle: { width: 0 }, showSymbol: false, areaStyle: { opacity: 0.8 }, data: dataAnxiety },
            { name: '허무주의', type: 'line', stack: 'Total', smooth: true, lineStyle: { width: 0 }, showSymbol: false, areaStyle: { opacity: 0.8 }, data: dataNihilism }
        ]
    };
    
    myChart.setOption(option);
    window.addEventListener('resize', () => myChart.resize());
}

// 7. 지식 서랍(Drawer) 열기 로직
function openDrawer(keyword) {
    const drawer = document.getElementById('paperDrawer');
    const overlay = document.getElementById('drawerOverlay');
    const targetEl = document.getElementById('drawerKeywordTarget');
    const contentEl = document.getElementById('drawerContent');
    
    if(!drawer) return;

    targetEl.innerText = keyword;
    drawer.classList.add('open');
    if(overlay) overlay.classList.add('open');
    
    // 내용 채우기 (로딩 연출)
    contentEl.innerHTML = '<div style="text-align:center; padding: 3rem; color:#94a3b8;"><span class="status-dot"></span><br><br>연관 KCI 문헌 검색 중...</div>';
    
    setTimeout(() => {
        let papers = [];
        if (globalData && globalData.focus_gauge) {
            papers = globalData.focus_gauge.filter(p => p.title.includes(keyword) || p.author.includes(keyword));
            if(papers.length === 0) {
                // UI 데모 목적: 완전히 안 겹치면 랜덤하게 연관 논문처럼 노출
                const shuffled = [...globalData.focus_gauge].sort(() => 0.5 - Math.random());
                papers = shuffled.slice(0, 3);
            }
        }
        
        if (papers.length === 0) {
            contentEl.innerHTML = '<div style="text-align:center; padding: 2rem; color:#ff4757;">검색된 연관 문헌이 없습니다. 새로운 연구 공백입니다!</div>';
            return;
        }

        let html = '';
        papers.forEach(p => {
            // Mock 초록 연출
            const abstract = `이 연구는 기존의 담론을 해체하고, <strong>'${keyword}'</strong>의 관점에서 실존주의와 철학적 지형의 구조적 한계를 조망합니다. 특히 ${p.author}의 논지를 바탕으로 어떻게 주체가 자유를 실천할 수 있는지 분석하며...`;
            
            html += `
            <div class="drawer-item" onclick="window.open('https://scholar.google.co.kr/scholar?q=${encodeURIComponent(p.title)}', '_blank')">
                <div class="drawer-item-title">${p.title} <span style="font-size: 0.8em; opacity:0.6; margin-left:4px;">↗</span></div>
                <div class="drawer-item-authors">${p.author} | ${p.journal} | 피인용 ${p.citations}회</div>
                <div class="drawer-item-abstract">${abstract}</div>
            </div>`;
        });
        contentEl.innerHTML = html;
    }, 600); // 0.6초 로딩
}
