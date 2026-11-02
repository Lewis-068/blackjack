import streamlit as st
import random

st.set_page_config(page_title="Blackjack")

if 'page' not in st.session_state:
  st.session_state['page'] = 'main'
if st.session_state['page'] != 'blackjack' and 'dealer' in st.session_state:
  del st.session_state['dealer']
if st.session_state['page'] != 'blackjack' and 'player' in st.session_state:
  del st.session_state['player']
if st.session_state['page'] != 'blackjack' and 'rate' in st.session_state:
  del st.session_state['rate']

text, _, button = st.columns([2, 7, 2])
with text:
    code = st.text_input("secret code: ")
    if st.button("코드 확인"):
      elif code.lower() == "general":
        st.session_state['page'] = 'blackjack0'
      elif code.lower() == "KDHBYD":
        st.session_state['page'] = 'blackjack1'
      elif code.lower() == "DUVGEG":
        st.session_state['page'] = 'blackjack2'
      elif code.lower() == "VTQFVS":
        st.session_state['page'] = 'blackjack3'
      elif code == "":
        st.toast("코드를 입력해주세요.")
      else:
        st.toast("코드가 올바르지 않습니다.")

def show_blackjack0():
  st.title("블랙잭")
  st.write("가진 카드의 합이 21을 넘지 않으면서 딜러보다 21에 더 가까이 만들면 승리하는 게임입니다.")
  st.caption("개발자가 코딩하기 귀찮은 관계로 간소화된 룰을 적용합니다.")
  st.caption("코딩의 편의를 위해 항상 A 카드는 맨 뒤에 배치됩니다.")
  with st.expander("룰 설명"):
    st.write("1. 플레이어와 딜러가 각각 카드를 두 장씩 받습니다(Dealing). 이때, 딜러의 두번째 카드는 비공개합니다.")
    st.write("2. 플레이어는 자신의 카드를 보고 카드를 더 받을 지(Hit), 차례를 마칠 지(Stay) 결정합니다.")
    st.caption("이때, A는 1또는 11 중 플레이어에게 유리한 수로, K Q J는 10으로 적용합니다.")
    st.caption("만일 플레이어의 첫 패가 A와 10(10, K, Q, J)일 경우 곧바로 21이 되어 승리하며, 이 패를 '블랙잭'이라고 합니다.")
    st.caption("블랙잭으로 승리할 경우 최종 승률 계산에서 1.5회 승리로 간주합니다.")
    st.caption("현재 숫자가 21을 넘지(Bust)않는 이상, 원하는 만큼 카드를 더 받을 수 있습니다.")
    st.write("3.차례가 끝나고 카드의 수를 합산한 결과, 21을 넘을 경우 딜러의 패에 관계없이 반드시 패배합니다.")
    st.write("4.차례가 끝난 후 21을 넘지 않았다면 딜러가 카드를 받으며, 이때 딜러가 버스트하거나 플레이어의 총합이 딜러의 총합보다 21에 더 가까우면 플레이어가 승리합니다.")
    st.caption("딜러는 16 이하에서 무조건 히트, 17 이상에서 스테이합니다.")
    st.caption("버스트되지 않는 한, 딜러의 A 카드는 11로 계산합니다.")
    st.write("5. 서렌더(Surrender)는 플레이어가 딜링 단계일 때만 가능합니다.")
    st.caption("서렌더는 최종 승률 계산에서 0.5회 패배로 간주합니다.")
  deck =  ['A', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
  if 'dealer' not in st.session_state:
    st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
  if 'player' not in st.session_state:
    st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
  if 'rate' not in st.session_state:
    st.session_state['rate'] = {'match':0, 'win':0, 'blackjack':0, 'push':0, 'lose':0, 'surrender':0}
  def sumcard(subject):
    st.session_state[subject]['sum'] = 0
    st.session_state[subject]['card'].sort(key=lambda x: x == 'A')
    A_count = st.session_state[subject]['card'].count('A')
    for card in st.session_state[subject]['card']:
      if card == 'K' or card == 'Q' or card == 'J':
        st.session_state[subject]['sum'] += 10
      elif isinstance(card, int):
        st.session_state[subject]['sum'] += card
      elif card == 'A':
        if st.session_state[subject]['sum'] <= (11 - A_count):
          st.session_state[subject]['sum'] += 11
        elif st.session_state[subject]['sum'] > (11 - A_count):
          st.session_state[subject]['sum'] += 1
        A_count -= 1
  def judgement():
    if st.session_state['player']['sum'] > 21:
      st.session_state['player']['state'] = '버스트(패배)'
      st.session_state['dealer']['state'] = '승리'
      st.session_state['rate']['lose'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['dealer']['sum'] > 21:
      st.session_state['dealer']['state'] = '버스트(패배)'
      st.session_state['player']['state'] = '승리'
      st.session_state['rate']['win'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] > st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '패배'
      st.session_state['player']['state'] = '승리'
      st.session_state['rate']['win'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] < st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '승리'
      st.session_state['player']['state'] = '패배'
      st.session_state['rate']['lose'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] == st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '무승부'
      st.session_state['player']['state'] = '무승부'
      st.session_state['rate']['push'] +=1
      st.session_state['rate']['match'] +=1
  
  with st.container(border=True):
    st.markdown('### 딜러')
    st.caption(f'상태: {st.session_state['dealer']['state']}')
    st.write(f"현재 패: {st.session_state['dealer']['card']}")
  with st.container(border=True):
    st.markdown('### 플레이어')
    st.caption(f'상태: {st.session_state['player']['state']}')
    st.write(f"현재 패: {st.session_state['player']['card']}")
    if st.session_state['dealer']['state'] == None:
      if st.button('딜링', use_container_width=True):
        st.session_state['dealer']['state'] = '딜링'
        st.session_state['player']['state'] = '딜링' 
        st.session_state['dealer']['card'].append(random.choice(deck))
        st.session_state['dealer']['card'].append('?')
        st.session_state['player']['card'].append(random.choice(deck))
        st.session_state['player']['card'].append(random.choice(deck))
        sumcard('player')
        if st.session_state['player']['sum'] == 21:
          st.session_state['player']['state'] = '블랙잭!'
          st.session_state['dealer']['state'] = '패배'
          st.session_state['rate']['win'] +=1
          st.session_state['rate']['blackjack'] +=1
          st.session_state['rate']['match'] +=1
        st.rerun()
    if st.session_state['dealer']['state'] == '딜링' and st.session_state['player']['state'] != '스테이':
      hit, stay = st.columns(2)
      with hit:
        if st.button('히트', use_container_width=True):
          st.session_state['player']['state'] = '히트'
          st.session_state['player']['card'].append(random.choice(deck))
          sumcard('player')
          if st.session_state['player']['sum'] > 21:
            st.session_state['player']['state'] = '버스트(패배)'
            st.session_state['dealer']['state'] = '승리'
            st.session_state['rate']['lose'] += 1
            st.session_state['rate']['match'] += 1
            st.rerun()
          else:
            st.rerun()
      with stay:
        if st.button('스테이', use_container_width=True):
          st.session_state['player']['state'] = '스테이'
          st.rerun()
    if st.session_state['player']['state'] == '스테이':
        st.session_state['dealer']['state'] = '히트'
        st.session_state['dealer']['card'].remove('?')
        st.session_state['dealer']['card'].append(random.choice(deck))
        sumcard('dealer')
        if st.session_state['dealer']['sum'] == 21:
            st.session_state['dealer']['state'] = '블랙잭!'
            st.session_state['player']['state'] = '패배'
            st.session_state['rate']['lose'] +=1
            st.session_state['rate']['match'] +=1
        else:
          while st.session_state['dealer']['sum'] < 17:
            st.session_state['dealer']['card'].append(random.choice(deck))
            sumcard('dealer')
          judgement()
        st.rerun()
    

  rerun, clear = st.columns(2)
  with rerun:
    if st.button("돌아가기"):
        st.session_state['page'] = 'main'
        st.rerun()
  with clear:
    if st.session_state['player']['state'] == '승리' or st.session_state['player']['state'] == '패배' or st.session_state['dealer']['state'] == '승리' or st.session_state['dealer']['state'] == '패배' or st.session_state['player']['state'] == None or st.session_state['dealer']['state'] == None or st.session_state['player']['state'] == '무승부' or st.session_state['dealer']['state'] == '무승부':
      if st.button("게임 초기화"):
        st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
        st.rerun()
    elif st.session_state['player']['state'] == '딜링':
      if st.button("서렌더"):
        st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['rate']['lose'] +=1
        st.session_state['rate']['surrender'] +=1
        st.session_state['rate']['match'] +=1
        st.rerun()
  win = st.session_state['rate']['win']
  blackjack = st.session_state['rate']['blackjack']
  push = st.session_state['rate']['push']
  lose = st.session_state['rate']['lose']
  surrender = st.session_state['rate']['surrender']
  match = st.session_state['rate']['match']
  match2 = (win - blackjack) + 1.5 * blackjack + push + (lose - surrender) + 0.5 * surrender
  if match2 == 0:
    rate = 0
  else:
    rate = (((win - blackjack) + 1.5 * blackjack + push/2) / match2) * 100
  st.write(f"현재 승률:{rate: .2f}% ({match}전 {win}승 {push}무 {lose}패) // 블랙잭: {blackjack}회, 서렌더: {surrender}회")
  st.caption("이 페이지를 나가면 승률이 초기화됩니다.")

def show_blackjack1():
  st.title("블랙잭")
  st.write("가진 카드의 합이 21을 넘지 않으면서 딜러보다 21에 더 가까이 만들면 승리하는 게임입니다.")
  st.caption("개발자가 코딩하기 귀찮은 관계로 간소화된 룰을 적용합니다.")
  st.caption("코딩의 편의를 위해 항상 A 카드는 맨 뒤에 배치됩니다.")
  with st.expander("룰 설명"):
    st.write("1. 플레이어와 딜러가 각각 카드를 두 장씩 받습니다(Dealing). 이때, 딜러의 두번째 카드는 비공개합니다.")
    st.write("2. 플레이어는 자신의 카드를 보고 카드를 더 받을 지(Hit), 차례를 마칠 지(Stay) 결정합니다.")
    st.caption("이때, A는 1또는 11 중 플레이어에게 유리한 수로, K Q J는 10으로 적용합니다.")
    st.caption("만일 플레이어의 첫 패가 A와 10(10, K, Q, J)일 경우 곧바로 21이 되어 승리하며, 이 패를 '블랙잭'이라고 합니다.")
    st.caption("블랙잭으로 승리할 경우 최종 승률 계산에서 1.5회 승리로 간주합니다.")
    st.caption("현재 숫자가 21을 넘지(Bust)않는 이상, 원하는 만큼 카드를 더 받을 수 있습니다.")
    st.write("3.차례가 끝나고 카드의 수를 합산한 결과, 21을 넘을 경우 딜러의 패에 관계없이 반드시 패배합니다.")
    st.write("4.차례가 끝난 후 21을 넘지 않았다면 딜러가 카드를 받으며, 이때 딜러가 버스트하거나 플레이어의 총합이 딜러의 총합보다 21에 더 가까우면 플레이어가 승리합니다.")
    st.caption("딜러는 16 이하에서 무조건 히트, 17 이상에서 스테이합니다.")
    st.caption("버스트되지 않는 한, 딜러의 A 카드는 11로 계산합니다.")
    st.write("5. 서렌더(Surrender)는 플레이어가 딜링 단계일 때만 가능합니다.")
    st.caption("서렌더는 최종 승률 계산에서 0.5회 패배로 간주합니다.")
  deck =  ['A', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
  if 'dealer' not in st.session_state:
    st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
  if 'player' not in st.session_state:
    st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
  if 'rate' not in st.session_state:
    st.session_state['rate'] = {'match':0, 'win':0, 'blackjack':0, 'push':0, 'lose':0, 'surrender':0}
  def sumcard(subject):
    st.session_state[subject]['sum'] = 0
    st.session_state[subject]['card'].sort(key=lambda x: x == 'A')
    A_count = st.session_state[subject]['card'].count('A')
    for card in st.session_state[subject]['card']:
      if card == 'K' or card == 'Q' or card == 'J':
        st.session_state[subject]['sum'] += 10
      elif isinstance(card, int):
        st.session_state[subject]['sum'] += card
      elif card == 'A':
        if st.session_state[subject]['sum'] <= (11 - A_count):
          st.session_state[subject]['sum'] += 11
        elif st.session_state[subject]['sum'] > (11 - A_count):
          st.session_state[subject]['sum'] += 1
        A_count -= 1
  def judgement():
    if st.session_state['player']['sum'] > 21:
      st.session_state['player']['state'] = '버스트(패배)'
      st.session_state['dealer']['state'] = '승리'
      st.session_state['rate']['lose'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['dealer']['sum'] > 21:
      st.session_state['dealer']['state'] = '버스트(패배)'
      st.session_state['player']['state'] = '승리'
      st.session_state['rate']['win'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] > st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '패배'
      st.session_state['player']['state'] = '승리'
      st.session_state['rate']['win'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] < st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '승리'
      st.session_state['player']['state'] = '패배'
      st.session_state['rate']['lose'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] == st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '무승부'
      st.session_state['player']['state'] = '무승부'
      st.session_state['rate']['push'] +=1
      st.session_state['rate']['match'] +=1
  
  with st.container(border=True):
    st.markdown('### 딜러')
    st.caption(f'상태: {st.session_state['dealer']['state']}')
    st.write(f"현재 패: {st.session_state['dealer']['card']}")
  with st.container(border=True):
    st.markdown('### 플레이어')
    st.caption(f'상태: {st.session_state['player']['state']}')
    st.write(f"현재 패: {st.session_state['player']['card']}")
    if st.session_state['dealer']['state'] == None:
      if st.button('딜링', use_container_width=True):
        st.session_state['dealer']['state'] = '딜링'
        st.session_state['player']['state'] = '딜링' 
        st.session_state['dealer']['card'].append(random.choice(deck))
        st.session_state['dealer']['card'].append('?')
        st.session_state['player']['card'].append(random.choice(deck))
        st.session_state['player']['card'].append(random.choice(deck))
        sumcard('player')
        if st.session_state['player']['sum'] == 21:
          st.session_state['player']['state'] = '블랙잭!'
          st.session_state['dealer']['state'] = '패배'
          st.session_state['rate']['win'] +=1
          st.session_state['rate']['blackjack'] +=1
          st.session_state['rate']['match'] +=1
        st.rerun()
    if st.session_state['dealer']['state'] == '딜링' and st.session_state['player']['state'] != '스테이':
      hit, stay = st.columns(2)
      with hit:
        if st.button('히트', use_container_width=True):
          st.session_state['player']['state'] = '히트'
          st.session_state['player']['card'].append(random.choice(deck))
          sumcard('player')
          if st.session_state['player']['sum'] > 21:
            st.session_state['player']['state'] = '버스트(패배)'
            st.session_state['dealer']['state'] = '승리'
            st.session_state['rate']['lose'] += 1
            st.session_state['rate']['match'] += 1
            st.rerun()
          else:
            st.rerun()
      with stay:
        if st.button('스테이', use_container_width=True):
          st.session_state['player']['state'] = '스테이'
          st.rerun()
    if st.session_state['player']['state'] == '스테이':
        st.session_state['dealer']['state'] = '히트'
        st.session_state['dealer']['card'].remove('?')
        st.session_state['dealer']['card'].append(random.choice(deck))
        sumcard('dealer')
        if st.session_state['dealer']['sum'] == 21:
            st.session_state['dealer']['state'] = '블랙잭!'
            st.session_state['player']['state'] = '패배'
            st.session_state['rate']['lose'] +=1
            st.session_state['rate']['match'] +=1
        else:
          while st.session_state['dealer']['sum'] < 17:
            st.session_state['dealer']['card'].append(random.choice(deck))
            sumcard('dealer')
          judgement()
        st.rerun()
    

  rerun, clear = st.columns(2)
  with rerun:
    if st.button("돌아가기"):
        st.session_state['page'] = 'main'
        st.rerun()
  with clear:
    if st.session_state['player']['state'] == '승리' or st.session_state['player']['state'] == '패배' or st.session_state['dealer']['state'] == '승리' or st.session_state['dealer']['state'] == '패배' or st.session_state['player']['state'] == None or st.session_state['dealer']['state'] == None or st.session_state['player']['state'] == '무승부' or st.session_state['dealer']['state'] == '무승부':
      if st.button("게임 초기화"):
        st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
        st.rerun()
    elif st.session_state['player']['state'] == '딜링':
      if st.button("서렌더"):
        st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['rate']['lose'] +=1
        st.session_state['rate']['surrender'] +=1
        st.session_state['rate']['match'] +=1
        st.rerun()
  win = st.session_state['rate']['win']
  blackjack = st.session_state['rate']['blackjack']
  push = st.session_state['rate']['push']
  lose = st.session_state['rate']['lose']
  surrender = st.session_state['rate']['surrender']
  match = st.session_state['rate']['match']
  match2 = (win - blackjack) + 1.5 * blackjack + push + (lose - surrender) + 0.5 * surrender
  if match2 == 0:
    rate = 0
  else:
    rate = (((win - blackjack) + 1.5 * blackjack + push/2) / match2) * 100
  st.write(f"현재 승률:{rate: .2f}% ({match}전 {win}승 {push}무 {lose}패) // 블랙잭: {blackjack}회, 서렌더: {surrender}회")
  st.caption("이 페이지를 나가면 승률이 초기화됩니다.")
  st.caption("등록 플레이어: 맹상수 / 코드번호:4636647")

def show_blackjack2():
  st.title("블랙잭")
  st.write("가진 카드의 합이 21을 넘지 않으면서 딜러보다 21에 더 가까이 만들면 승리하는 게임입니다.")
  st.caption("개발자가 코딩하기 귀찮은 관계로 간소화된 룰을 적용합니다.")
  st.caption("코딩의 편의를 위해 항상 A 카드는 맨 뒤에 배치됩니다.")
  with st.expander("룰 설명"):
    st.write("1. 플레이어와 딜러가 각각 카드를 두 장씩 받습니다(Dealing). 이때, 딜러의 두번째 카드는 비공개합니다.")
    st.write("2. 플레이어는 자신의 카드를 보고 카드를 더 받을 지(Hit), 차례를 마칠 지(Stay) 결정합니다.")
    st.caption("이때, A는 1또는 11 중 플레이어에게 유리한 수로, K Q J는 10으로 적용합니다.")
    st.caption("만일 플레이어의 첫 패가 A와 10(10, K, Q, J)일 경우 곧바로 21이 되어 승리하며, 이 패를 '블랙잭'이라고 합니다.")
    st.caption("블랙잭으로 승리할 경우 최종 승률 계산에서 1.5회 승리로 간주합니다.")
    st.caption("현재 숫자가 21을 넘지(Bust)않는 이상, 원하는 만큼 카드를 더 받을 수 있습니다.")
    st.write("3.차례가 끝나고 카드의 수를 합산한 결과, 21을 넘을 경우 딜러의 패에 관계없이 반드시 패배합니다.")
    st.write("4.차례가 끝난 후 21을 넘지 않았다면 딜러가 카드를 받으며, 이때 딜러가 버스트하거나 플레이어의 총합이 딜러의 총합보다 21에 더 가까우면 플레이어가 승리합니다.")
    st.caption("딜러는 16 이하에서 무조건 히트, 17 이상에서 스테이합니다.")
    st.caption("버스트되지 않는 한, 딜러의 A 카드는 11로 계산합니다.")
    st.write("5. 서렌더(Surrender)는 플레이어가 딜링 단계일 때만 가능합니다.")
    st.caption("서렌더는 최종 승률 계산에서 0.5회 패배로 간주합니다.")
  deck =  ['A', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
  if 'dealer' not in st.session_state:
    st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
  if 'player' not in st.session_state:
    st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
  if 'rate' not in st.session_state:
    st.session_state['rate'] = {'match':0, 'win':0, 'blackjack':0, 'push':0, 'lose':0, 'surrender':0}
  def sumcard(subject):
    st.session_state[subject]['sum'] = 0
    st.session_state[subject]['card'].sort(key=lambda x: x == 'A')
    A_count = st.session_state[subject]['card'].count('A')
    for card in st.session_state[subject]['card']:
      if card == 'K' or card == 'Q' or card == 'J':
        st.session_state[subject]['sum'] += 10
      elif isinstance(card, int):
        st.session_state[subject]['sum'] += card
      elif card == 'A':
        if st.session_state[subject]['sum'] <= (11 - A_count):
          st.session_state[subject]['sum'] += 11
        elif st.session_state[subject]['sum'] > (11 - A_count):
          st.session_state[subject]['sum'] += 1
        A_count -= 1
  def judgement():
    if st.session_state['player']['sum'] > 21:
      st.session_state['player']['state'] = '버스트(패배)'
      st.session_state['dealer']['state'] = '승리'
      st.session_state['rate']['lose'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['dealer']['sum'] > 21:
      st.session_state['dealer']['state'] = '버스트(패배)'
      st.session_state['player']['state'] = '승리'
      st.session_state['rate']['win'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] > st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '패배'
      st.session_state['player']['state'] = '승리'
      st.session_state['rate']['win'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] < st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '승리'
      st.session_state['player']['state'] = '패배'
      st.session_state['rate']['lose'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] == st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '무승부'
      st.session_state['player']['state'] = '무승부'
      st.session_state['rate']['push'] +=1
      st.session_state['rate']['match'] +=1
  
  with st.container(border=True):
    st.markdown('### 딜러')
    st.caption(f'상태: {st.session_state['dealer']['state']}')
    st.write(f"현재 패: {st.session_state['dealer']['card']}")
  with st.container(border=True):
    st.markdown('### 플레이어')
    st.caption(f'상태: {st.session_state['player']['state']}')
    st.write(f"현재 패: {st.session_state['player']['card']}")
    if st.session_state['dealer']['state'] == None:
      if st.button('딜링', use_container_width=True):
        st.session_state['dealer']['state'] = '딜링'
        st.session_state['player']['state'] = '딜링' 
        st.session_state['dealer']['card'].append(random.choice(deck))
        st.session_state['dealer']['card'].append('?')
        st.session_state['player']['card'].append(random.choice(deck))
        st.session_state['player']['card'].append(random.choice(deck))
        sumcard('player')
        if st.session_state['player']['sum'] == 21:
          st.session_state['player']['state'] = '블랙잭!'
          st.session_state['dealer']['state'] = '패배'
          st.session_state['rate']['win'] +=1
          st.session_state['rate']['blackjack'] +=1
          st.session_state['rate']['match'] +=1
        st.rerun()
    if st.session_state['dealer']['state'] == '딜링' and st.session_state['player']['state'] != '스테이':
      hit, stay = st.columns(2)
      with hit:
        if st.button('히트', use_container_width=True):
          st.session_state['player']['state'] = '히트'
          st.session_state['player']['card'].append(random.choice(deck))
          sumcard('player')
          if st.session_state['player']['sum'] > 21:
            st.session_state['player']['state'] = '버스트(패배)'
            st.session_state['dealer']['state'] = '승리'
            st.session_state['rate']['lose'] += 1
            st.session_state['rate']['match'] += 1
            st.rerun()
          else:
            st.rerun()
      with stay:
        if st.button('스테이', use_container_width=True):
          st.session_state['player']['state'] = '스테이'
          st.rerun()
    if st.session_state['player']['state'] == '스테이':
        st.session_state['dealer']['state'] = '히트'
        st.session_state['dealer']['card'].remove('?')
        st.session_state['dealer']['card'].append(random.choice(deck))
        sumcard('dealer')
        if st.session_state['dealer']['sum'] == 21:
            st.session_state['dealer']['state'] = '블랙잭!'
            st.session_state['player']['state'] = '패배'
            st.session_state['rate']['lose'] +=1
            st.session_state['rate']['match'] +=1
        else:
          while st.session_state['dealer']['sum'] < 17:
            st.session_state['dealer']['card'].append(random.choice(deck))
            sumcard('dealer')
          judgement()
        st.rerun()
    

  rerun, clear = st.columns(2)
  with rerun:
    if st.button("돌아가기"):
        st.session_state['page'] = 'main'
        st.rerun()
  with clear:
    if st.session_state['player']['state'] == '승리' or st.session_state['player']['state'] == '패배' or st.session_state['dealer']['state'] == '승리' or st.session_state['dealer']['state'] == '패배' or st.session_state['player']['state'] == None or st.session_state['dealer']['state'] == None or st.session_state['player']['state'] == '무승부' or st.session_state['dealer']['state'] == '무승부':
      if st.button("게임 초기화"):
        st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
        st.rerun()
    elif st.session_state['player']['state'] == '딜링':
      if st.button("서렌더"):
        st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['rate']['lose'] +=1
        st.session_state['rate']['surrender'] +=1
        st.session_state['rate']['match'] +=1
        st.rerun()
  win = st.session_state['rate']['win']
  blackjack = st.session_state['rate']['blackjack']
  push = st.session_state['rate']['push']
  lose = st.session_state['rate']['lose']
  surrender = st.session_state['rate']['surrender']
  match = st.session_state['rate']['match']
  match2 = (win - blackjack) + 1.5 * blackjack + push + (lose - surrender) + 0.5 * surrender
  if match2 == 0:
    rate = 0
  else:
    rate = (((win - blackjack) + 1.5 * blackjack + push/2) / match2) * 100
  st.write(f"현재 승률:{rate: .2f}% ({match}전 {win}승 {push}무 {lose}패) // 블랙잭: {blackjack}회, 서렌더: {surrender}회")
  st.caption("이 페이지를 나가면 승률이 초기화됩니다.")
  st.caption("등록 플레이어: 최민상 / 코드번호: 4377843")

def show_blackjack2():
  st.title("블랙잭")
  st.write("가진 카드의 합이 21을 넘지 않으면서 딜러보다 21에 더 가까이 만들면 승리하는 게임입니다.")
  st.caption("개발자가 코딩하기 귀찮은 관계로 간소화된 룰을 적용합니다.")
  st.caption("코딩의 편의를 위해 항상 A 카드는 맨 뒤에 배치됩니다.")
  with st.expander("룰 설명"):
    st.write("1. 플레이어와 딜러가 각각 카드를 두 장씩 받습니다(Dealing). 이때, 딜러의 두번째 카드는 비공개합니다.")
    st.write("2. 플레이어는 자신의 카드를 보고 카드를 더 받을 지(Hit), 차례를 마칠 지(Stay) 결정합니다.")
    st.caption("이때, A는 1또는 11 중 플레이어에게 유리한 수로, K Q J는 10으로 적용합니다.")
    st.caption("만일 플레이어의 첫 패가 A와 10(10, K, Q, J)일 경우 곧바로 21이 되어 승리하며, 이 패를 '블랙잭'이라고 합니다.")
    st.caption("블랙잭으로 승리할 경우 최종 승률 계산에서 1.5회 승리로 간주합니다.")
    st.caption("현재 숫자가 21을 넘지(Bust)않는 이상, 원하는 만큼 카드를 더 받을 수 있습니다.")
    st.write("3.차례가 끝나고 카드의 수를 합산한 결과, 21을 넘을 경우 딜러의 패에 관계없이 반드시 패배합니다.")
    st.write("4.차례가 끝난 후 21을 넘지 않았다면 딜러가 카드를 받으며, 이때 딜러가 버스트하거나 플레이어의 총합이 딜러의 총합보다 21에 더 가까우면 플레이어가 승리합니다.")
    st.caption("딜러는 16 이하에서 무조건 히트, 17 이상에서 스테이합니다.")
    st.caption("버스트되지 않는 한, 딜러의 A 카드는 11로 계산합니다.")
    st.write("5. 서렌더(Surrender)는 플레이어가 딜링 단계일 때만 가능합니다.")
    st.caption("서렌더는 최종 승률 계산에서 0.5회 패배로 간주합니다.")
  deck =  ['A', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
  if 'dealer' not in st.session_state:
    st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
  if 'player' not in st.session_state:
    st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
  if 'rate' not in st.session_state:
    st.session_state['rate'] = {'match':0, 'win':0, 'blackjack':0, 'push':0, 'lose':0, 'surrender':0}
  def sumcard(subject):
    st.session_state[subject]['sum'] = 0
    st.session_state[subject]['card'].sort(key=lambda x: x == 'A')
    A_count = st.session_state[subject]['card'].count('A')
    for card in st.session_state[subject]['card']:
      if card == 'K' or card == 'Q' or card == 'J':
        st.session_state[subject]['sum'] += 10
      elif isinstance(card, int):
        st.session_state[subject]['sum'] += card
      elif card == 'A':
        if st.session_state[subject]['sum'] <= (11 - A_count):
          st.session_state[subject]['sum'] += 11
        elif st.session_state[subject]['sum'] > (11 - A_count):
          st.session_state[subject]['sum'] += 1
        A_count -= 1
  def judgement():
    if st.session_state['player']['sum'] > 21:
      st.session_state['player']['state'] = '버스트(패배)'
      st.session_state['dealer']['state'] = '승리'
      st.session_state['rate']['lose'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['dealer']['sum'] > 21:
      st.session_state['dealer']['state'] = '버스트(패배)'
      st.session_state['player']['state'] = '승리'
      st.session_state['rate']['win'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] > st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '패배'
      st.session_state['player']['state'] = '승리'
      st.session_state['rate']['win'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] < st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '승리'
      st.session_state['player']['state'] = '패배'
      st.session_state['rate']['lose'] +=1
      st.session_state['rate']['match'] +=1
    elif st.session_state['player']['sum'] == st.session_state['dealer']['sum']:
      st.session_state['dealer']['state'] = '무승부'
      st.session_state['player']['state'] = '무승부'
      st.session_state['rate']['push'] +=1
      st.session_state['rate']['match'] +=1
  
  with st.container(border=True):
    st.markdown('### 딜러')
    st.caption(f'상태: {st.session_state['dealer']['state']}')
    st.write(f"현재 패: {st.session_state['dealer']['card']}")
  with st.container(border=True):
    st.markdown('### 플레이어')
    st.caption(f'상태: {st.session_state['player']['state']}')
    st.write(f"현재 패: {st.session_state['player']['card']}")
    if st.session_state['dealer']['state'] == None:
      if st.button('딜링', use_container_width=True):
        st.session_state['dealer']['state'] = '딜링'
        st.session_state['player']['state'] = '딜링' 
        st.session_state['dealer']['card'].append(random.choice(deck))
        st.session_state['dealer']['card'].append('?')
        st.session_state['player']['card'].append(random.choice(deck))
        st.session_state['player']['card'].append(random.choice(deck))
        sumcard('player')
        if st.session_state['player']['sum'] == 21:
          st.session_state['player']['state'] = '블랙잭!'
          st.session_state['dealer']['state'] = '패배'
          st.session_state['rate']['win'] +=1
          st.session_state['rate']['blackjack'] +=1
          st.session_state['rate']['match'] +=1
        st.rerun()
    if st.session_state['dealer']['state'] == '딜링' and st.session_state['player']['state'] != '스테이':
      hit, stay = st.columns(2)
      with hit:
        if st.button('히트', use_container_width=True):
          st.session_state['player']['state'] = '히트'
          st.session_state['player']['card'].append(random.choice(deck))
          sumcard('player')
          if st.session_state['player']['sum'] > 21:
            st.session_state['player']['state'] = '버스트(패배)'
            st.session_state['dealer']['state'] = '승리'
            st.session_state['rate']['lose'] += 1
            st.session_state['rate']['match'] += 1
            st.rerun()
          else:
            st.rerun()
      with stay:
        if st.button('스테이', use_container_width=True):
          st.session_state['player']['state'] = '스테이'
          st.rerun()
    if st.session_state['player']['state'] == '스테이':
        st.session_state['dealer']['state'] = '히트'
        st.session_state['dealer']['card'].remove('?')
        st.session_state['dealer']['card'].append(random.choice(deck))
        sumcard('dealer')
        if st.session_state['dealer']['sum'] == 21:
            st.session_state['dealer']['state'] = '블랙잭!'
            st.session_state['player']['state'] = '패배'
            st.session_state['rate']['lose'] +=1
            st.session_state['rate']['match'] +=1
        else:
          while st.session_state['dealer']['sum'] < 17:
            st.session_state['dealer']['card'].append(random.choice(deck))
            sumcard('dealer')
          judgement()
        st.rerun()
    

  rerun, clear = st.columns(2)
  with rerun:
    if st.button("돌아가기"):
        st.session_state['page'] = 'main'
        st.rerun()
  with clear:
    if st.session_state['player']['state'] == '승리' or st.session_state['player']['state'] == '패배' or st.session_state['dealer']['state'] == '승리' or st.session_state['dealer']['state'] == '패배' or st.session_state['player']['state'] == None or st.session_state['dealer']['state'] == None or st.session_state['player']['state'] == '무승부' or st.session_state['dealer']['state'] == '무승부':
      if st.button("게임 초기화"):
        st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
        st.rerun()
    elif st.session_state['player']['state'] == '딜링':
      if st.button("서렌더"):
        st.session_state['dealer'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['player'] = {'card':[], 'sum':0, 'state':None}
        st.session_state['rate']['lose'] +=1
        st.session_state['rate']['surrender'] +=1
        st.session_state['rate']['match'] +=1
        st.rerun()
  win = st.session_state['rate']['win']
  blackjack = st.session_state['rate']['blackjack']
  push = st.session_state['rate']['push']
  lose = st.session_state['rate']['lose']
  surrender = st.session_state['rate']['surrender']
  match = st.session_state['rate']['match']
  match2 = (win - blackjack) + 1.5 * blackjack + push + (lose - surrender) + 0.5 * surrender
  if match2 == 0:
    rate = 0
  else:
    rate = (((win - blackjack) + 1.5 * blackjack + push/2) / match2) * 100
  st.write(f"현재 승률:{rate: .2f}% ({match}전 {win}승 {push}무 {lose}패) // 블랙잭: {blackjack}회, 서렌더: {surrender}회")
  st.caption("이 페이지를 나가면 승률이 초기화됩니다.")
  st.caption("등록 플레이어: 최은준 / 코드번호: 6661664")

if st.session_state['page'] == 'main':
    show_main_page()
elif st.session_state['page'] == 'blackjack0':
    show_blackjack0()
elif st.session_state['page'] == 'blackjack1':
    show_blackjack1()
elif st.session_state['page'] == 'blackjack2':
    show_blackjack2()
elif st.session_state['page'] == 'blackjack3':
    show_blackjack3()
