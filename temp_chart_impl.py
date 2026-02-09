
# 2. Add this functional implementation for the grouped evolution chart
# This can be pasted into app_streamlit.py above the front-end section

def plot_evolution_bars(df):
    """
    Plots a grouped bar chart for SP and MS evolution with floating annotations
    for Entradas (+) and Saídas (-).
    """
    # 1. Prepare Data
    # Get all unique months in order of appearance
    unique_months = df['Mes_Ref'].unique()
    
    # Calculate balances for SP
    df_sp = df[df['Estado'] == 'SP']
    sp_balances = []
    sp_entradas = []
    sp_saidas = []
    
    # Get initial balance for SP (assuming first entry's Saldo_Inicial is the start)
    if not df_sp.empty:
        curr_balance = df_sp.iloc[0]['Saldo_Inicial']
        for _, row in df_sp.iterrows():
            # Balance at end of month = Start + In - Out
            # If curr_balance is start of month:
            curr_balance = curr_balance + row['Entrada'] - row['Saida']
            sp_balances.append(curr_balance)
            sp_entradas.append(row['Entrada'])
            sp_saidas.append(row['Saida'])
    
    # Calculate balances for MS
    df_ms = df[df['Estado'] == 'MS']
    ms_balances = []
    ms_entradas = []
    ms_saidas = []
    
    if not df_ms.empty:
        curr_balance = df_ms.iloc[0]['Saldo_Inicial']
        for _, row in df_ms.iterrows():
            curr_balance = curr_balance + row['Entrada'] - row['Saida']
            ms_balances.append(curr_balance)
            ms_entradas.append(row['Entrada'])
            ms_saidas.append(row['Saida'])

    # Align data to unique_months (handle missing months if any, though assumed aligned)
    # For simplicity, assuming df is well-formed with same months for both or we just plot what we have.
    # We will plot based on the lists.
    
    fig = go.Figure()

    # SP Bars
    fig.add_trace(go.Bar(
        name='SP',
        x=unique_months,
        y=sp_balances,
        marker_color=COR_CHART_BLUE, # Dark Blue
        text=sp_balances,
        textposition='outside',
        textfont=dict(color='white', size=14, family='JetBrains Mono')
    ))

    # MS Bars
    fig.add_trace(go.Bar(
        name='MS',
        x=unique_months,
        y=ms_balances,
        marker_color=COR_PRIMARY, # Cocal Green
        text=ms_balances,
        textposition='outside',
        textfont=dict(color='white', size=14, family='JetBrains Mono')
    ))

    # Add Annotations (Floating Boxes)
    # We add them for SP and MS.
    # Calculating positions: Shift x slightly for grouped bars.
    # Plotly Grouped Bars: by default, they share the x-tick.
    # We can use 'x' as the month, and 'xanchor' adjustments or offsetgroups?
    # Easier: Just loop and add annotations.
    # Note: Precise positioning over grouped bars in Plotly can be tricky with just 'x'.
    # Alternative: Use a scatter trace with text mode for the boxes?
    # Or just use standard annotations.
    
    # Let's try standard annotations.
    # Problem: knowing the exact X coordinate of the "SP" bar vs "MS" bar.
    # In Plotly, if x='Jan', the bars are side-by-side centered on 'Jan'.
    # SP is left, MS is right.
    # We can approximate with xoffset? No, annotations don't strictly support xoffset in categorical axes easily.
    # BETTER APPROACH: USE SCATTER TRACES for the boxes.
    # We can specify 'offsetgroup'? No.
    
    # Workaround: Plotly automatically places bars.
    # If we want to place text exactly over the bars, we can use the 'text' property of the bars themselves!
    # BUT we are already using 'text' for the Balance Value (e.g. 503).
    # The user wants a box with +73/-215 floating ABOVE the bar.
    # We can append this to the text?
    # "<b>503</b><br><span style='font-size:10px; background-color:white; color:black'>...</span>"
    # This might mess up the "outside" positioning cleanliness.
    
    # Let's try appending the box info to the text, but formatted nicely.
    # Or, use a second scatter trace that is invisible but has text.
    # For grouped bars, we can manage X positions if we use numerical X axis, but here it's categorical.
    
    # HACK: The User Image shows the box FLOATING well above.
    # Let's try simpler first: Just replace the 'text' with the whole block?
    # Value + Box.
    # "503<br><br><span style='...'>+73<br>-215</span>"
    # The gap <br><br> lifts the box.
    
    def format_box(val, ent, sai):
        # formatted HTML for the text
        # box style: white background, shadow... 
        # Plotly HTML subset is limited. Background color for specific span is NOT supported properly in SVG text.
        # We can only color text.
        # We can use a Scatter trace with marker symbol 'square' or custom SVG as background? Too complex.
        
        # Simpler approach: Just the text numbers with colors, maybe a unicode box?
        # Or just text.
        return f"<b>{val}</b><br><br><span style='color:{COR_DANGER}'>+{ent}</span><br><span style='color:{COR_SUCCESS}'>-{sai}</span>"

    sp_texts = [format_box(b, e, s) for b, e, s in zip(sp_balances, sp_entradas, sp_saidas)]
    ms_texts = [format_box(b, e, s) for b, e, s in zip(ms_balances, ms_entradas, ms_saidas)]
    
    # Update traces with new text
    fig.data[0].text = sp_texts
    fig.data[1].text = ms_texts
    
    fig.update_layout(
        title="Evolução de Saldo (Entradas vs Saídas)",
        title_font=dict(color='#FFFFFF'),
        barmode='group',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Outfit', 'color': '#FFFFFF'},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#FFFFFF')
        ),
        xaxis=dict(showgrid=False, color='#FFFFFF', tickfont=dict(color='#FFFFFF')),
        yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.1)', color='#FFFFFF', tickfont=dict(color='#FFFFFF')),
        margin=dict(t=60, b=40, l=40, r=40)
    )
    
    return fig
