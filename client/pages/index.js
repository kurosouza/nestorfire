import React, { useState } from 'react';
import Head from 'next/head';
import dynamic from 'next/dynamic';
import { Grommet, Anchor, Box, Heading, Paragraph, TextInput, Text, Select, Form, FormField } from 'grommet';

const Map = dynamic(() => import('../components/Map'), { ssr: false });

export default () => {

  const [selected, setSelected] = useState('');

  const options = [];

  return (
    <>
      <Head>
        <link rel="stylesheet" href="/leaflet.css" type="text/css" />
      </Head>

      
        <Box align="center" margin="small" direction='column'>
          <Box align='center' direction='row' gap='small' >
            <Text>Date</Text>

            <Select id='dateS' name='dateS' value={selected} onChange={({ opt }) => { setSelected(opt); }}
              options={options}
            />

            <Text>offset</Text>
            <TextInput value={10} />
            <Text>limit</Text>
            <TextInput value={10} />

          </Box>
          <Box margin="small" size='large' >

            <Map />

          </Box>

          <Heading>Grommet is awesome!</Heading>
          <Paragraph>
            Find out more at{' '}
            <Anchor href="https://v2.grommet.io/">https://v2.grommet.io/</Anchor>
          </Paragraph>
        </Box>
      
    </>
  );

}
