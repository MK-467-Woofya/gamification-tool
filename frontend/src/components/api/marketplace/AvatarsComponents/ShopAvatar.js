import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { BuyButton } from "./BuyButton";

/**
 * Single Avatar display component.
 * For use with the Avatar Page
 */
export const ShopAvatar = ({ user, avatar, setUser }) => {

    return (
        <Container>   
            <Row className="align-items-center">
                <Col>
                    <img src={avatar.img_url} alt={avatar.name} width={192} height={192}/>
                </Col>
                <Col>
                    <h2>{avatar.name}</h2>
                    <p>Partner: {avatar.partner}</p>
                    <p>Description: {avatar.description}</p>
                </Col>
                <Col>
                    <p>Avatar listed: {avatar.is_listed.toString()}</p>
                    <p>Cost: {avatar.cost}</p>
                </Col>
                <Col>
                    <p>Buy {avatar.name}:</p>
                    <BuyButton user={user} avatar={avatar} setUser={setUser}/>
                </Col>
            </Row>
        </Container>
    );
};
