import logo from './logo.svg';
import './App.css';

import styled from "styled-components";

export const Header = () => {
    const HeaderContainer = styled.header`
        background: #F38A0E;
    `

    return <HeaderContainer>
        <img src="./Group 1 1.svg" alt=""/>
    </HeaderContainer>
}

export const Card = ({plane_id, status, point_from, point_to, bus_id, changeDriver, time_from, time_to}) => {
    const CardContainer = styled.div`
        border-top: 10px #F38A0E solid;
        box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    `

    const CardHeader = styled.header`
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        
        padding: 5px 10px;
    `

    const PlaneId = styled.span`
        display: block;
        
        font-size: 26px;
        line-height: 31px;
    `;

    const Separator = styled.div`
        height: 1px;
        filter: blur(1px);
        background: #F0EEEE;
    `

    const CardBody = styled.div`
        display: flex;
        flex-direction: row;
        padding: 10px;
        
        gap: 10px;
    `

    const Left = styled.div`
        flex: 2 0;
        display: flex;
        flex-direction: column;
        gap: 10px;
    `

    const Right = styled(Left)`
        flex: 1 0;
    `

    const Dest = styled.div`
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        padding: 5px 10px;
        
        background: #928E8E;
        border-radius: 5px;
    `

    const DestName = styled.span`
        font-size: 16px;
        line-height: 19px;
        color: #fff;
    `

    const DestTime = styled.span`
        padding: 5px 10px;
        color: #fff;
        background: #A5A5A5; 
        border-radius: 5px;
    `

    const BusId = styled(Dest)`
        text-align: center;
        justify-content: center;
    `

    const Button = styled.button`
        outline: none;
        border: none;
        background: none;
        
        font-size: 16px;
        line-height: 35px;
        
        padding; 5px 10px;
        
        background: #F38A0E;
        color: #fff;
        
        border-radius: 5px;
    `

    return <CardContainer>
        <CardHeader>
            <PlaneId>
                {`Рейс-${plane_id}`}
            </PlaneId>
            <PlaneId>
                {status}
            </PlaneId>
        </CardHeader>
        <Separator></Separator>
        <CardBody>
            <Left>
                <Dest>
                    <DestName>{point_from}</DestName><DestTime>{time_from}</DestTime>
                </Dest>
                <Dest>
                    <DestName>{point_to}</DestName><DestTime>{time_to}</DestTime>
                </Dest>
            </Left>
            <Right>
                <BusId>
                    <DestName style={{lineHeight: '25px'}}>Автобус - {bus_id}</DestName>
                </BusId>
                <Button>
                    Сменить водителя
                </Button>
            </Right>
        </CardBody>
    </CardContainer>
}

export const Cards = () => {
    const CardsContainer = styled.section`
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
        grid-gap: 25px;
    `

    return <CardsContainer>
        <Card plane_id={124} status={'ЕЗ'} point_from={'test from'} point_to={'test to'} bus_id={'5'}
              changeDriver={() => {
              }} time_from={'8:20'} time_to={'8:20'}></Card>
        <Card plane_id={124} status={'ЕЗ'} point_from={'test from'} point_to={'test to'} bus_id={'5'}
              changeDriver={() => {
              }} time_from={'8:20'} time_to={'8:20'}></Card>
        <Card plane_id={124} status={'ЕЗ'} point_from={'test from'} point_to={'test to'} bus_id={'5'}
              changeDriver={() => {
              }} time_from={'8:20'} time_to={'8:20'}></Card>
        <Card plane_id={124} status={'ЕЗ'} point_from={'test from'} point_to={'test to'} bus_id={'5'}
              changeDriver={() => {
              }} time_from={'8:20'} time_to={'8:20'}></Card>
        <Card plane_id={124} status={'ЕЗ'} point_from={'test from'} point_to={'test to'} bus_id={'5'}
              changeDriver={() => {
              }} time_from={'8:20'} time_to={'8:20'}></Card>
        <Card plane_id={124} status={'ЕЗ'} point_from={'test from'} point_to={'test to'} bus_id={'5'}
              changeDriver={() => {
              }} time_from={'8:20'} time_to={'8:20'}></Card>
        <Card plane_id={124} status={'ЕЗ'} point_from={'test from'} point_to={'test to'} bus_id={'5'}
              changeDriver={() => {
              }} time_from={'8:20'} time_to={'8:20'}></Card>
    </CardsContainer>
}

export const Main = () => {
    const MainContainer = styled.main`
        padding: 50px;
    `

    return <MainContainer>
        <Cards/>
    </MainContainer>
}

export const App = () => {
    return (
        <>
            <Header/>
            <Main/>
        </>
    );
}

export default App;
