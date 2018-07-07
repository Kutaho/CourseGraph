import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addCount, serverRenderClock, startClock } from '../utils/store';
import Page from '../components/Page';

class Counter extends React.Component {
    static async getInitialProps({store, isServer}) {
        store.dispatch(serverRenderClock(isServer));
        store.dispatch(addCount());

        return {isServer};
    }

    static propTypes = {
        startClock: PropTypes.func,
    };

    componentDidMount() {
        this.timer = this.props.startClock();
    }

    componentWillUnmount() {
        clearInterval(this.timer);
    }

    render() {
        return (
            <Page title='Index Page' linkTo='/other'/>
        );
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        addCount: bindActionCreators(addCount, dispatch),
        startClock: bindActionCreators(startClock, dispatch)
    };
};

export default connect(null, mapDispatchToProps)(Counter);
