'use client'

import React, {useEffect, useState} from 'react'
import { PdfUploader } from '@/components/pdf-uploader'

function Page() {

  const [data, setData] = useState("Loading");

  useEffect(() => {
    fetch('http://localhost:8080/api/home')
      .then(response => response.json())
      .then(data => setData(data.message))
  }, [])

  return (
    <div>
      <div>{data}</div>
      <PdfUploader />
      <SalesFunnel />
    </div>
  )
}

export default Page;
