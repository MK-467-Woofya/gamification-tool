import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { BuyButton } from "./BuyButton";

/**
 * Single Title display component.
 * For use with the Avatar Page
 */
export const ShopTitle = ({ user, title, setUser }) => {

    return (
        <Container>   
            <Row className="align-items-center">
                <Col>
                    <h2>{title.text}</h2>
                    <p>Name identifier: {title.name}</p>
                    <p>Partner: {title.partner}</p>
                </Col>
                <Col>
                    <p>Description: {title.description}</p>
                    <p>Title listed: {title.is_listed.toString()}</p>
                    <p>Cost: {title.cost}</p>
                </Col>
                <Col>
                    <p>Buy {title.name}:</p>
                    <BuyButton user={user} title={title} setUser={setUser}/>
                </Col>
            </Row>
        </Container>
    );
};
