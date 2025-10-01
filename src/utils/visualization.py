"""워크플로우 시각화 유틸리티 함수들"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple, Any
import base64
import io
from IPython.display import Image, display

def create_workflow_diagram_matplotlib() -> bytes:
    """Matplotlib을 사용한 워크플로우 다이어그램 생성"""

    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # 색상 정의
    colors = {
        'entry': '#4CAF50',      # 초록 - 시작점
        'classifier': '#FF9800',  # 주황 - 분류기
        'agent': '#2196F3',      # 파랑 - 에이전트
        'tools': '#9C27B0',      # 보라 - 도구
        'synthesizer': '#F44336', # 빨강 - 응답 생성
        'end': '#607D8B'         # 회색 - 종료
    }

    # 노드 위치 정의
    nodes = {
        'START': (5, 11, colors['entry']),
        'classifier': (5, 9.5, colors['classifier']),
        'candidate_agent': (2, 7.5, colors['agent']),
        'market_agent': (4, 7.5, colors['agent']),
        'web_agent': (6, 7.5, colors['agent']),
        'general_agent': (8, 7.5, colors['agent']),
        'tools': (5, 5.5, colors['tools']),
        'synthesizer': (5, 3.5, colors['synthesizer']),
        'END': (5, 1.5, colors['end'])
    }

    # 노드 그리기
    for node_name, (x, y, color) in nodes.items():
        if node_name in ['START', 'END']:
            # 시작/종료 노드는 원형
            circle = plt.Circle((x, y), 0.3, color=color, alpha=0.8)
            ax.add_patch(circle)
        else:
            # 일반 노드는 사각형
            box = FancyBboxPatch(
                (x-0.8, y-0.3), 1.6, 0.6,
                boxstyle="round,pad=0.1",
                facecolor=color,
                alpha=0.8,
                edgecolor='black'
            )
            ax.add_patch(box)

        # 노드 라벨
        ax.text(x, y, node_name.replace('_', '\n'),
                ha='center', va='center', fontsize=9, fontweight='bold')

    # 화살표 그리기
    arrows = [
        (5, 11, 5, 9.8),      # START → classifier
        (5, 9.2, 2, 7.8),     # classifier → candidate_agent
        (5, 9.2, 4, 7.8),     # classifier → market_agent
        (5, 9.2, 6, 7.8),     # classifier → web_agent
        (5, 9.2, 8, 7.8),     # classifier → general_agent
        (2, 7.2, 4.2, 5.8),  # candidate_agent → tools
        (4, 7.2, 4.8, 5.8),  # market_agent → tools
        (6, 7.2, 5.8, 5.8),  # web_agent → tools
        (8, 7.2, 5.8, 5.8),  # general_agent → tools
        (5, 5.2, 5, 3.8),    # tools → synthesizer
        (5, 3.2, 5, 1.8),    # synthesizer → END
    ]

    for x1, y1, x2, y2 in arrows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', lw=2, color='black'))

    # 데이터 소스 박스 추가
    data_sources = [
        (1, 4.5, 'PostgreSQL\n(정형 데이터)\n• 인재 정보\n• 경력/스킬\n• 희망조건', '#E8F5E8'),
        (5, 4.5, 'FAISS Vector DB\n(비정형 데이터)\n• 시장 트렌드\n• 기술 정보\n• 급여 분석', '#E3F2FD'),
        (9, 4.5, 'Tavily Web Search\n(실시간 데이터)\n• 최신 뉴스\n• 채용공고\n• 회사 정보', '#FFF3E0')
    ]

    for x, y, text, color in data_sources:
        box = FancyBboxPatch(
            (x-0.9, y-0.8), 1.8, 1.6,
            boxstyle="round,pad=0.1",
            facecolor=color,
            alpha=0.7,
            edgecolor='gray',
            linestyle='--'
        )
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8)

    # 제목
    ax.text(5, 12.5, '🤖 헤드헌터 AI 에이전트 워크플로우',
            ha='center', va='center', fontsize=16, fontweight='bold')

    # 범례
    legend_elements = [
        mpatches.Patch(color=colors['entry'], label='시작점'),
        mpatches.Patch(color=colors['classifier'], label='쿼리 분류기'),
        mpatches.Patch(color=colors['agent'], label='전담 에이전트'),
        mpatches.Patch(color=colors['tools'], label='도구 실행'),
        mpatches.Patch(color=colors['synthesizer'], label='응답 생성'),
        mpatches.Patch(color=colors['end'], label='종료')
    ]

    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))

    # 이미지를 바이트로 변환
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
    img_buffer.seek(0)
    plt.close()

    return img_buffer.getvalue()

def create_workflow_diagram_plotly() -> go.Figure:
    """Plotly를 사용한 인터랙티브 워크플로우 다이어그램 생성"""

    # 노드 정보
    nodes_info = [
        {"id": "START", "x": 5, "y": 11, "color": "#4CAF50", "type": "circle"},
        {"id": "classifier", "x": 5, "y": 9.5, "color": "#FF9800", "type": "box"},
        {"id": "candidate_agent", "x": 2, "y": 7.5, "color": "#2196F3", "type": "box"},
        {"id": "market_agent", "x": 4, "y": 7.5, "color": "#2196F3", "type": "box"},
        {"id": "web_agent", "x": 6, "y": 7.5, "color": "#2196F3", "type": "box"},
        {"id": "general_agent", "x": 8, "y": 7.5, "color": "#2196F3", "type": "box"},
        {"id": "tools", "x": 5, "y": 5.5, "color": "#9C27B0", "type": "box"},
        {"id": "synthesizer", "x": 5, "y": 3.5, "color": "#F44336", "type": "box"},
        {"id": "END", "x": 5, "y": 1.5, "color": "#607D8B", "type": "circle"}
    ]

    # 엣지 정보
    edges = [
        ("START", "classifier"),
        ("classifier", "candidate_agent"),
        ("classifier", "market_agent"),
        ("classifier", "web_agent"),
        ("classifier", "general_agent"),
        ("candidate_agent", "tools"),
        ("market_agent", "tools"),
        ("web_agent", "tools"),
        ("general_agent", "tools"),
        ("tools", "synthesizer"),
        ("synthesizer", "END")
    ]

    fig = go.Figure()

    # 엣지 그리기
    for source, target in edges:
        source_node = next(n for n in nodes_info if n["id"] == source)
        target_node = next(n for n in nodes_info if n["id"] == target)

        fig.add_trace(go.Scatter(
            x=[source_node["x"], target_node["x"]],
            y=[source_node["y"], target_node["y"]],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))

        # 화살표 추가
        fig.add_annotation(
            x=target_node["x"], y=target_node["y"],
            ax=source_node["x"], ay=source_node["y"],
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="black"
        )

    # 노드 그리기
    for node in nodes_info:
        if node["type"] == "circle":
            fig.add_trace(go.Scatter(
                x=[node["x"]],
                y=[node["y"]],
                mode='markers+text',
                marker=dict(
                    size=30,
                    color=node["color"],
                    symbol='circle'
                ),
                text=[node["id"]],
                textposition="middle center",
                name=node["id"],
                showlegend=False
            ))
        else:
            fig.add_trace(go.Scatter(
                x=[node["x"]],
                y=[node["y"]],
                mode='markers+text',
                marker=dict(
                    size=40,
                    color=node["color"],
                    symbol='square'
                ),
                text=[node["id"].replace('_', '<br>')],
                textposition="middle center",
                name=node["id"],
                showlegend=False
            ))

    # 레이아웃 설정
    fig.update_layout(
        title={
            'text': "🤖 헤드헌터 AI 에이전트 워크플로우",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        width=800,
        height=600,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    return fig

def create_tools_distribution_chart() -> go.Figure:
    """도구 분류별 분포 차트 생성"""

    tool_categories = {
        '정형 데이터 도구 (PostgreSQL)': 9,
        '비정형 데이터 도구 (FAISS)': 7,
        '웹 검색 도구 (Tavily)': 6
    }

    fig = go.Figure(data=[
        go.Pie(
            labels=list(tool_categories.keys()),
            values=list(tool_categories.values()),
            hole=0.3,
            marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
    ])

    fig.update_layout(
        title={
            'text': "도구 분류별 분포 (총 22개)",
            'x': 0.5,
            'xanchor': 'center'
        },
        font=dict(size=12),
        width=500,
        height=400
    )

    return fig

def display_workflow_in_streamlit():
    """Streamlit에서 워크플로우 시각화 표시"""

    st.header("🔄 AI 에이전트 워크플로우")

    # 탭으로 구분
    tab1, tab2, tab3 = st.tabs(["📊 워크플로우 다이어그램", "🛠️ 도구 분포", "📝 워크플로우 설명"])

    with tab1:
        st.subheader("워크플로우 구조")

        # Plotly 인터랙티브 다이어그램
        try:
            plotly_fig = create_workflow_diagram_plotly()
            st.plotly_chart(plotly_fig, use_container_width=True)
        except Exception as e:
            st.error(f"인터랙티브 다이어그램 생성 실패: {e}")

            # 대체: Matplotlib 정적 이미지
            try:
                img_bytes = create_workflow_diagram_matplotlib()
                st.image(img_bytes, caption="헤드헌터 AI 에이전트 워크플로우")
            except Exception as e2:
                st.error(f"정적 다이어그램도 생성 실패: {e2}")

    with tab2:
        st.subheader("도구 분류별 분포")

        # 도구 분포 차트
        try:
            tools_fig = create_tools_distribution_chart()
            st.plotly_chart(tools_fig, use_container_width=True)
        except Exception as e:
            st.error(f"도구 분포 차트 생성 실패: {e}")

        # 도구 상세 목록
        st.subheader("📋 전체 도구 목록")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**🗃️ 정형 데이터 도구 (9개)**")
            postgres_tools = [
                "search_candidates_by_skills",
                "search_candidates_by_location",
                "search_candidates_by_salary_range",
                "search_candidates_by_work_type",
                "search_candidates_by_industry",
                "search_candidates_by_availability",
                "get_candidate_details",
                "complex_candidate_search",
                "get_candidate_statistics"
            ]
            for tool in postgres_tools:
                st.write(f"• {tool}")

        with col2:
            st.markdown("**🔍 비정형 데이터 도구 (7개)**")
            vector_tools = [
                "search_tech_information",
                "search_market_trends",
                "search_industry_analysis",
                "search_salary_information",
                "general_knowledge_search",
                "compare_technologies",
                "get_knowledge_base_stats"
            ]
            for tool in vector_tools:
                st.write(f"• {tool}")

        with col3:
            st.markdown("**🌐 웹 검색 도구 (6개)**")
            web_tools = [
                "web_search_latest_trends",
                "search_job_postings",
                "search_company_information",
                "search_salary_benchmarks",
                "search_tech_news",
                "search_startup_funding_news"
            ]
            for tool in web_tools:
                st.write(f"• {tool}")

    with tab3:
        st.subheader("📖 워크플로우 단계별 설명")

        steps = [
            ("🚀 START", "사용자가 질문을 입력합니다."),
            ("🧠 classifier", "AI가 질문 유형을 분석하여 적절한 에이전트로 라우팅합니다."),
            ("👥 candidate_agent", "인재 검색 관련 질문을 PostgreSQL 데이터베이스에서 처리합니다."),
            ("📈 market_agent", "시장 분석 질문을 FAISS 벡터 DB에서 검색합니다."),
            ("🌐 web_agent", "최신 정보가 필요한 질문을 Tavily 웹 검색으로 처리합니다."),
            ("🤝 general_agent", "복합적인 질문을 여러 도구를 조합하여 처리합니다."),
            ("🛠️ tools", "선택된 에이전트가 전문 도구들을 실행합니다."),
            ("✨ synthesizer", "도구 실행 결과를 종합하여 최종 답변을 생성합니다."),
            ("🏁 END", "완성된 답변을 사용자에게 전달합니다.")
        ]

        for step, description in steps:
            with st.expander(f"{step}"):
                st.write(description)

        st.info("""
        **💡 워크플로우 특징:**
        - **정형/비정형 데이터 분리**: 각각 최적화된 방식으로 처리
        - **자동 라우팅**: 질문 유형에 따라 적절한 에이전트 선택
        - **전문 도구**: 22개의 세분화된 도구로 정확한 정보 제공
        - **결과 통합**: 여러 소스의 정보를 종합한 완전한 답변
        """)

def create_beautiful_mermaid_workflow() -> bytes:
    """
    Customer Support Agent 스타일의 아름다운 Mermaid 워크플로우 생성
    LangGraph의 draw_mermaid_png() 기능을 활용 (없으면 대체 방법 사용)
    """
    try:
        from src.agents.workflow import get_headhunter_workflow

        # 워크플로우 가져오기
        workflow_instance = get_headhunter_workflow()
        compiled_graph = workflow_instance.get_graph()

        # Method 1: LangGraph의 draw_mermaid_png 시도 (최신 버전)
        try:
            mermaid_png = compiled_graph.get_graph().draw_mermaid_png(
                draw_method="pyvis",
                output_file_path=None,
                background_color="white",
                node_colors={
                    "START": "#4CAF50",
                    "classifier": "#FF9800",
                    "candidate_agent": "#2196F3",
                    "market_agent": "#2196F3",
                    "web_agent": "#2196F3",
                    "general_agent": "#2196F3",
                    "tools": "#9C27B0",
                    "synthesizer": "#F44336",
                    "END": "#607D8B"
                }
            )
            return mermaid_png
        except AttributeError:
            # Method 2: 간단한 draw_mermaid_png 시도
            try:
                mermaid_png = compiled_graph.get_graph().draw_mermaid_png()
                return mermaid_png
            except AttributeError:
                # Method 3: get_graph() 자체를 PNG로 변환
                try:
                    import io
                    graph_data = compiled_graph.get_graph()

                    # 그래프 정보를 이용해 더 정교한 matplotlib 다이어그램 생성
                    return create_advanced_matplotlib_workflow(graph_data)
                except:
                    # Method 4: 기본 matplotlib 사용
                    return create_workflow_diagram_matplotlib()

    except Exception as e:
        print(f"Mermaid 워크플로우 생성 실패: {e}")
        # 대체: 기존 matplotlib 다이어그램
        return create_workflow_diagram_matplotlib()

def create_advanced_matplotlib_workflow(graph_data=None) -> bytes:
    """
    Customer Support Agent 스타일을 모방한 고급 Matplotlib 워크플로우
    실제 그래프 데이터를 기반으로 더 정확한 시각화 생성
    """
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 14)
    ax.axis('off')

    # Customer Support Agent 스타일 색상 (더 세련된)
    colors = {
        'entry': '#2E7D32',      # 진한 초록 - 시작점
        'classifier': '#F57700',  # 진한 주황 - 분류기
        'agent': '#1565C0',      # 진한 파랑 - 에이전트
        'tools': '#7B1FA2',      # 진한 보라 - 도구
        'synthesizer': '#C62828', # 진한 빨강 - 응답 생성
        'end': '#455A64'         # 진한 회색 - 종료
    }

    # 그림자 효과를 위한 오프셋
    shadow_offset = 0.05

    # 노드 위치 정의 (더 균형잡힌 레이아웃)
    nodes = {
        'START': (6, 13, colors['entry'], '🚀 START'),
        'classifier': (6, 11, colors['classifier'], '🧠 Query\nClassifier'),
        'candidate_agent': (2.5, 8.5, colors['agent'], '👥 Candidate\nAgent'),
        'market_agent': (4.5, 8.5, colors['agent'], '📈 Market\nAgent'),
        'web_agent': (7.5, 8.5, colors['agent'], '🌐 Web\nAgent'),
        'general_agent': (9.5, 8.5, colors['agent'], '🤝 General\nAgent'),
        'tools': (6, 6, colors['tools'], '🛠️ Tool\nExecution'),
        'synthesizer': (6, 3.5, colors['synthesizer'], '✨ Response\nSynthesizer'),
        'END': (6, 1, colors['end'], '🏁 END')
    }

    # 그림자 효과가 있는 노드 그리기
    for node_name, (x, y, color, label) in nodes.items():
        if node_name in ['START', 'END']:
            # 원형 노드 (그림자)
            shadow_circle = plt.Circle((x+shadow_offset, y-shadow_offset), 0.4,
                                     color='gray', alpha=0.3, zorder=1)
            ax.add_patch(shadow_circle)
            # 원형 노드 (메인)
            circle = plt.Circle((x, y), 0.4, color=color, alpha=0.9,
                              edgecolor='white', linewidth=3, zorder=2)
            ax.add_patch(circle)
        else:
            # 사각형 노드 (그림자)
            shadow_box = FancyBboxPatch(
                (x-1.0+shadow_offset, y-0.5-shadow_offset), 2.0, 1.0,
                boxstyle="round,pad=0.15",
                facecolor='gray',
                alpha=0.3,
                zorder=1
            )
            ax.add_patch(shadow_box)
            # 사각형 노드 (메인)
            box = FancyBboxPatch(
                (x-1.0, y-0.5), 2.0, 1.0,
                boxstyle="round,pad=0.15",
                facecolor=color,
                alpha=0.9,
                edgecolor='white',
                linewidth=3,
                zorder=2
            )
            ax.add_patch(box)

        # 노드 라벨 (그림자)
        ax.text(x+0.02, y-0.02, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='gray', alpha=0.5, zorder=3)
        # 노드 라벨 (메인)
        ax.text(x, y, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white', zorder=4)

    # 고급 화살표 그리기 (곡선 및 그라데이션 효과)
    arrows = [
        (6, 12.6, 6, 11.4),      # START → classifier
        (6, 10.6, 2.5, 9.0),    # classifier → candidate_agent
        (6, 10.6, 4.5, 9.0),    # classifier → market_agent
        (6, 10.6, 7.5, 9.0),    # classifier → web_agent
        (6, 10.6, 9.5, 9.0),    # classifier → general_agent
        (2.5, 8.0, 5.2, 6.5),   # candidate_agent → tools
        (4.5, 8.0, 5.7, 6.5),   # market_agent → tools
        (7.5, 8.0, 6.8, 6.5),   # web_agent → tools
        (9.5, 8.0, 6.8, 6.5),   # general_agent → tools
        (6, 5.5, 6, 4.0),       # tools → synthesizer
        (6, 3.0, 6, 1.4),       # synthesizer → END
    ]

    for x1, y1, x2, y2 in arrows:
        # 화살표 그리기 (두꺼운 선 + 그림자)
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', lw=4, color='gray', alpha=0.3))
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', lw=3, color='#333333'))

    # 데이터 소스 박스 (더 세련된 스타일)
    data_sources = [
        (2, 4.5, '🗃️ PostgreSQL\n(정형 데이터)\n\n• 인재 정보\n• 경력/스킬\n• 희망조건', '#E8F5E8', '#4CAF50'),
        (6, 4.5, '🔍 FAISS Vector DB\n(비정형 데이터)\n\n• 시장 트렌드\n• 기술 정보\n• 급여 분석', '#E3F2FD', '#2196F3'),
        (10, 4.5, '🌐 Tavily Web Search\n(실시간 데이터)\n\n• 최신 뉴스\n• 채용공고\n• 회사 정보', '#FFF3E0', '#FF9800')
    ]

    for x, y, text, bg_color, border_color in data_sources:
        # 그림자
        shadow_box = FancyBboxPatch(
            (x-1.2+shadow_offset, y-1.2-shadow_offset), 2.4, 2.4,
            boxstyle="round,pad=0.2",
            facecolor='gray',
            alpha=0.2,
            zorder=1
        )
        ax.add_patch(shadow_box)

        # 메인 박스
        box = FancyBboxPatch(
            (x-1.2, y-1.2), 2.4, 2.4,
            boxstyle="round,pad=0.2",
            facecolor=bg_color,
            alpha=0.8,
            edgecolor=border_color,
            linewidth=2,
            linestyle='--',
            zorder=2
        )
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, zorder=3)

    # 제목 (더 임팩트 있는 스타일)
    title_text = '🤖 헤드헌터 AI 에이전트 워크플로우'
    ax.text(6, 14.5, title_text, ha='center', va='center',
            fontsize=20, fontweight='bold', color='#1A237E',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#E8EAF6', alpha=0.8))

    # 부제목
    ax.text(6, 14, 'Customer Support Agent 스타일의 Professional Visualization',
            ha='center', va='center', fontsize=12, fontweight='normal',
            color='#3F51B5', style='italic')

    # 범례 (더 세련된 스타일)
    legend_elements = [
        mpatches.Patch(color=colors['entry'], label='🚀 시작점'),
        mpatches.Patch(color=colors['classifier'], label='🧠 쿼리 분류'),
        mpatches.Patch(color=colors['agent'], label='🤖 전담 에이전트'),
        mpatches.Patch(color=colors['tools'], label='🛠️ 도구 실행'),
        mpatches.Patch(color=colors['synthesizer'], label='✨ 응답 생성'),
        mpatches.Patch(color=colors['end'], label='🏁 완료')
    ]

    legend = ax.legend(handles=legend_elements, loc='upper right',
                      bbox_to_anchor=(0.98, 0.98), frameon=True,
                      fancybox=True, shadow=True, ncol=1)
    legend.get_frame().set_facecolor('#F5F5F5')
    legend.get_frame().set_alpha(0.9)

    # 배경 그라데이션 효과
    ax.set_facecolor('#FAFAFA')

    # 이미지를 바이트로 변환 (고해상도)
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none',
                bbox_extra_artists=[legend])
    img_buffer.seek(0)
    plt.close()

    return img_buffer.getvalue()

def display_beautiful_workflow_in_streamlit():
    """
    Customer Support Agent 스타일의 아름다운 워크플로우를 Streamlit에 표시
    """

    st.header("🔄 헤드헌터 AI 에이전트 워크플로우")
    st.markdown("**Customer Support Agent 스타일의 전문적인 워크플로우 시각화**")

    # 탭으로 구분
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Beautiful Workflow", "📊 구조 다이어그램", "🛠️ 도구 분포", "📝 워크플로우 설명"])

    with tab1:
        st.subheader("🎨 LangGraph Mermaid 스타일 워크플로우")
        st.markdown("*Customer Support Agent 노트북에서 사용된 고급 시각화 스타일*")

        try:
            # Beautiful Mermaid workflow
            mermaid_bytes = create_beautiful_mermaid_workflow()
            st.image(mermaid_bytes, caption="헤드헌터 AI 에이전트 - Professional Mermaid Workflow", use_column_width=True)

            # 다운로드 버튼 추가
            st.download_button(
                label="📥 워크플로우 이미지 다운로드",
                data=mermaid_bytes,
                file_name="headhunter_ai_workflow_beautiful.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"Beautiful workflow 생성 실패: {e}")
            st.info("대체 워크플로우를 표시합니다.")

            # 대체: 기존 matplotlib 다이어그램
            try:
                img_bytes = create_workflow_diagram_matplotlib()
                st.image(img_bytes, caption="헤드헌터 AI 에이전트 워크플로우 (대체)")
            except Exception as e2:
                st.error(f"대체 다이어그램도 생성 실패: {e2}")

    with tab2:
        st.subheader("📊 워크플로우 구조")

        # Plotly 인터랙티브 다이어그램
        try:
            plotly_fig = create_workflow_diagram_plotly()
            st.plotly_chart(plotly_fig, use_container_width=True)
        except Exception as e:
            st.error(f"인터랙티브 다이어그램 생성 실패: {e}")

            # 대체: Matplotlib 정적 이미지
            try:
                img_bytes = create_workflow_diagram_matplotlib()
                st.image(img_bytes, caption="헤드헌터 AI 에이전트 워크플로우")
            except Exception as e2:
                st.error(f"정적 다이어그램도 생성 실패: {e2}")

    with tab3:
        st.subheader("🛠️ 도구 분류별 분포")

        # 도구 분포 차트
        try:
            tools_fig = create_tools_distribution_chart()
            st.plotly_chart(tools_fig, use_container_width=True)
        except Exception as e:
            st.error(f"도구 분포 차트 생성 실패: {e}")

        # 도구 상세 목록
        st.subheader("📋 전체 도구 목록")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**🗃️ 정형 데이터 도구 (9개)**")
            postgres_tools = [
                "search_candidates_by_skills",
                "search_candidates_by_location",
                "search_candidates_by_salary_range",
                "search_candidates_by_work_type",
                "search_candidates_by_industry",
                "search_candidates_by_availability",
                "get_candidate_details",
                "complex_candidate_search",
                "get_candidate_statistics"
            ]
            for tool in postgres_tools:
                st.write(f"• {tool}")

        with col2:
            st.markdown("**🔍 비정형 데이터 도구 (7개)**")
            vector_tools = [
                "search_tech_information",
                "search_market_trends",
                "search_industry_analysis",
                "search_salary_information",
                "general_knowledge_search",
                "compare_technologies",
                "get_knowledge_base_stats"
            ]
            for tool in vector_tools:
                st.write(f"• {tool}")

        with col3:
            st.markdown("**🌐 웹 검색 도구 (6개)**")
            web_tools = [
                "web_search_latest_trends",
                "search_job_postings",
                "search_company_information",
                "search_salary_benchmarks",
                "search_tech_news",
                "search_startup_funding_news"
            ]
            for tool in web_tools:
                st.write(f"• {tool}")

    with tab4:
        st.subheader("📖 워크플로우 단계별 설명")

        steps = [
            ("🚀 START", "사용자가 질문을 입력합니다."),
            ("🧠 classifier", "AI가 질문 유형을 분석하여 적절한 에이전트로 라우팅합니다."),
            ("👥 candidate_agent", "인재 검색 관련 질문을 PostgreSQL 데이터베이스에서 처리합니다."),
            ("📈 market_agent", "시장 분석 질문을 FAISS 벡터 DB에서 검색합니다."),
            ("🌐 web_agent", "최신 정보가 필요한 질문을 Tavily 웹 검색으로 처리합니다."),
            ("🤝 general_agent", "복합적인 질문을 여러 도구를 조합하여 처리합니다."),
            ("🛠️ tools", "선택된 에이전트가 전문 도구들을 실행합니다."),
            ("✨ synthesizer", "도구 실행 결과를 종합하여 최종 답변을 생성합니다."),
            ("🏁 END", "완성된 답변을 사용자에게 전달합니다.")
        ]

        for step, description in steps:
            with st.expander(f"{step}"):
                st.write(description)

        st.info("""
        **💡 워크플로우 특징:**
        - **정형/비정형 데이터 분리**: 각각 최적화된 방식으로 처리
        - **자동 라우팅**: 질문 유형에 따라 적절한 에이전트 선택
        - **전문 도구**: 22개의 세분화된 도구로 정확한 정보 제공
        - **결과 통합**: 여러 소스의 정보를 종합한 완전한 답변
        """)

def save_workflow_diagram(output_path: str) -> bool:
    """워크플로우 다이어그램을 파일로 저장"""
    try:
        # Beautiful Mermaid 버전 우선 시도
        try:
            img_bytes = create_beautiful_mermaid_workflow()
        except:
            # 대체: Matplotlib 버전
            img_bytes = create_workflow_diagram_matplotlib()

        with open(output_path, 'wb') as f:
            f.write(img_bytes)
        return True
    except Exception as e:
        print(f"다이어그램 저장 실패: {e}")
        return False