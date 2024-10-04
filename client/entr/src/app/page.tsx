'use client'

import React, {useEffect, useState} from 'react'
import { PdfUploader } from '@/components/pdf-uploader'


function Page() {
  const apiUrl = 'http://localhost:4000';
  const [data, setData] = useState("Loading");

  useEffect(() => {
    fetch(`${apiUrl}/api/home`)
      .then(response => response.json())
      .then(data => setData(data.message))
  }, [])

  return (
    <div>
      <div>{data}</div>
      <PdfUploader />
    </div>
  )
}

export default Page;
